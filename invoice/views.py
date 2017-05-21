#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import b64decode
from datetime import datetime
import re

from invoice.models import Product, InvoiceProduct, Invoice, InvoiceCustomProduct, Sales

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse

from django.http import JsonResponse
from django.core.files.base import ContentFile

from django.conf import settings
import subprocess

from printer import PDFCreator

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.views import generic
from django.utils.html import escape

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import ObjectDoesNotExist

from django.forms.models import model_to_dict

import json
import urllib


# TO-DO: - Check Chinese character database compatibility
#        - implementing 訂造單
#        - implementing discount  (DONE)
#        - implementing editable invoice  (DONE)
#        - implementing furniture colours and (maybe) furniture photos (DONE)


# return a queryset object with latest invoices accorded by invoice_id in acending order
def get_uncompleted_invoices(number_of_invoices):
    latest_invoices = Invoice.objects.filter(status='U').order_by('last_update')[:number_of_invoices]
    return latest_invoices


# return True if product was deleted, False if products were not deleted
def delete_invoice_product(invoice_id):
    if InvoiceProduct.objects.filter(invoice_id=invoice_id).count() != 0:
        try:
            InvoiceProduct.objects.filter(invoice_id=invoice_id).delete()
        except IndexError:
            return False
        else:
            return True
    else:
        return False


def delete_invoice_custom_product(invoice_id):
    print(invoice_id)
    invoice_custom_products = InvoiceCustomProduct.objects.filter(invoice_id=invoice_id)
    try:
        invoice_custom_products.delete()
    except IndexError:
        return False
    else:
        return True

def change_status(invoice_id, status):
    try:
        Invoice.objects.filter(pk=invoice_id).update(status=status)
    except IndexError:
        return False
    return True


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/invoice')

def user_group_check(user):
    return user.groups.filter(name="Sales").exists()

@user_passes_test(user_group_check, login_url='/accounts/login/')
def root(request):
    return render(request, 'invoice/index.html', {'user': request.user})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def delete(request):
    if request.method == "GET":
        invoice_id = request.GET.get("invoice")
        if invoice_validation(invoice_id):
            if change_status(invoice_id, Invoice.Deleted):
                return HttpResponseRedirect('/invoice/search/?search=' + invoice_id)
            else:
                return HttpResponse("Please enter a valid invoice id")
        else:
            return HttpResponse("Please enter a valid invoice id")
    else:
        return HttpResponse("error")

@user_passes_test(user_group_check, login_url='/accounts/login/')
def confirm(request):
    if request.method == "GET":
        invoice_id = request.GET.get("invoice")
        if invoice_validation(invoice_id):
            if change_status(invoice_id, Invoice.Completed):
                return HttpResponseRedirect('/invoice/search/?search=' + invoice_id)
            else:
                return HttpResponse("Please enter a valid invoice id")
        else:
            return HttpResponse("Please enter a valid invoice id")
    else:
        return HttpResponse("error")

@user_passes_test(user_group_check, login_url='/accounts/login/')
def drawing(request):
    if request.method == "GET":
        invoice_id = request.GET.get("invoice")
        try:
            invoice = Invoice.objects.filter(pk=invoice_id).values()[0]
        except IndexError:
            return False
        return JsonResponse({'image': invoice['drawing']})
    elif request.method == "POST":
        invoice_id = request.POST.get("invoice")
        try:
            invoice = Invoice.objects.filter(pk=invoice_id)
        except IndexError:
            return False
        else:
            _, image_data = request.POST['image'].split(',')
            image_data = b64decode(image_data)
            image_name = invoice_id + ".png"
            invoice.update(drawing=ContentFile(image_data, image_name))
            return JsonResponse({'success': True})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def choose_create_invoice(request):
    return render(request, 'invoice/choose_create_invoice.html', {})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def search_detail(request, invoice_id=-1):
    if request.method == "GET":
        if invoice_id is not -1:
            if invoice_validation(invoice_id):
                try:
                    invoice = Invoice.objects.get(pk=invoice_id)
                except IndexError:
                    return render(request, 'invoice/search.html', {'error': True})
                else:
                    invoice_products = InvoiceProduct.objects.filter(invoice_id=invoice_id)
                    custom_products = InvoiceCustomProduct.objects.filter(invoice_id=invoice_id)
                    return render(request, 'invoice/search.html', {'invoice': invoice, 'products': invoice_products, 'custom_products': custom_products})
            else:
                return render(request, 'invoice/search.html', {'error': True})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def search(request):
    if request.method == "GET":
        string = request.GET.get("search", '')
        category = request.GET.get("cat", '')
        invoice = request.GET.get("invoice", '')
        # category: address, name, number

        # if a invoice_id is provided show it's detail and products
        # else show the latest invoices created
        if string is not '':
            if category == "address":
                invoices = Invoice.objects.filter(address__contains=string)
            elif category == "name":
                invoices = Invoice.objects.filter(first_name__contains=string)
            elif category == "number":
                invoices = Invoice.objects.filter(contact_number__contains=string)
            elif category == "invoice_id":
                invoices = Invoice.objects.filter(invoice_id__contains=string)

            if invoices.exists():
                noi = 8
                nop = (invoices.count() / (noi + 1)) + 1
                page = int(request.GET.get("p", 1))

                first_item = noi*(page-1)
                last_item = noi*page
                if page == nop:
                    last_item = invoices.count()

                return render(request, 'invoice/search.html', {'invoices': invoices[first_item:last_item], 'current_page': page-1, 'pages': range(nop), 'cat': category, 'str': string})
            else:
                return render(request, 'invoice/search.html', {'error': True})

        else:
            return render(request, 'invoice/search.html', {
                'last_invoices': Invoice.objects.all().order_by("-last_update")[:10]})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def edit(request, invoice_id=-1):
    if request.method == "GET":
        # if a invoice_id is provided show it's detail and products
        # else show the latest invoices created
        if invoice_id is not -1:
            if invoice_validation(invoice_id):
                try:
                    invoice = Invoice.objects.get(pk=invoice_id)
                except IndexError:
                    return render(request, 'invoice/edit.html', {'error': True})
                else:
                    if not invoice.is_custom_made:
                        invoice_products = InvoiceProduct.objects.filter(invoice_id=invoice_id)
                        custom_products = InvoiceCustomProduct.objects.filter(invoice_id=invoice_id)
                        return render(request, 'invoice/edit.html',
                                      {'invoice': invoice, 'products': invoice_products, 'custom_products': custom_products})
                    else:
                        custom_products = InvoiceCustomProduct.objects.filter(invoice_id=invoice_id).values()
                        return render(request, 'invoice/edit_custom.html', {'invoice': invoice, 'products': custom_products})
            else:
                return render(request, 'invoice/edit.html', {'error': True})
        else:
            return render(request, 'invoice/edit.html', {'error': True})
    # if method is 'POST' or 'HEAD'
    else:
        # create a mutable copy of the POST item
        r = request.POST.copy()
        r.pop('csrfmiddlewaretoken', None)
        name = r.pop('firstName', None)[0]
        tel = r.pop('contactNum', None)[0]
        homeNum = r.pop('homeNum', None)[0]
        address = r.pop('address', None)[0]
        payment_type = r.pop('payment_type', None)[0]
        additional_note = r.pop('additional_note', None)[0]
        deposit = int(r.pop('deposit', None)[0])
        price = int(r.pop('price', None)[0])
        discount = int(r.pop('discount', None)[0])

        # check if the invoice_id is valid
        if invoice_validation(invoice_id):
            try:
                invoice = Invoice.objects.get(pk=invoice_id)
            except IndexError:
                return render(request, 'invoice/failure.html', {})
            else:
                delete_invoice_custom_product(invoice_id)
                delete_invoice_product(invoice_id)
                # value stores the json of the product
                for key, value in r.items():
                    # parse json string
                    # id , quantity , color , side_note

                    p_json = json.loads(value)
                    if p_json['custom'] is not True:
                        try:
                            p = Product.objects.get(pk=p_json['id'])
                        except IndexError:
                            return render(request, 'invoice/failure.html', {})
                        else:
                            quantity = p_json['quantity']
                            color = p_json['color']
                            side_note = urllib.unquote(str(p_json['side_note']))
                            # create a new InvoiceProduct record
                            i = InvoiceProduct(invoice=invoice, product=p,
                                               quantity=quantity, side_note=side_note, color=color)
                            i.save()
                    elif p_json['custom'] is True:
                        custom_name = urllib.unquote(str(p_json['name'])).decode('utf8')
                        custom_color = urllib.unquote(str(p_json['color']))
                        custom_side_note = urllib.unquote(str(p_json['side_note']))
                        custom_quantity = p_json['quantity']
                        custom_price = p_json['price']
                        i = InvoiceCustomProduct(invoice=invoice, name=custom_name, color=custom_color, side_note=custom_side_note,
                                                 quantity=custom_quantity, price=custom_price)
                        i.save()

        if is_input_valid(name, address, tel) and additional_note is not None and deposit is not None and price is not None and discount is not None:
            Invoice.objects.filter(pk=invoice_id).update(first_name=name, contact_number=tel, home_number=homeNum, address=address,
                           additional_note=additional_note, payment_type=payment_type, deposit=deposit,
                           total_amount=price, discount=discount, remaining=price-deposit-discount)
        else:
            return render(request, 'invoice/failure.html', {})

        return HttpResponseRedirect('/invoice/search/' + invoice_id)

@user_passes_test(user_group_check, login_url='/accounts/login/')
def check(request):
    if request.method == 'GET':
        waiting_invoice = Invoice.objects.filter(status=Invoice.Waiting)
        if waiting_invoice.count() > 0:
            return render(request, 'invoice/check.html', {'created': True, 'invoices': waiting_invoice})
        else:
            invoices = Invoice.objects.filter(status=Invoice.Uncompleted).order_by('-last_update');
            return render(request, 'invoice/check.html', {'created': False, 'invoices': invoices})
    else:
        waiting_invoice = Invoice.objects.filter(status=Invoice.Waiting)
        method = request.POST.get('method', '')
        if method == 'create':
            if waiting_invoice.count() == 0:
                invoices = Invoice.objects.filter(status=Invoice.Uncompleted)
                invoices.update(status=Invoice.Waiting)
        elif method == 'print':
            pdf = PDFCreator()
        elif method == 'confirm':
            waiting_invoice.update(status=Invoice.Completed)

        return HttpResponseRedirect(reverse('invoice:check'))

@user_passes_test(user_group_check, login_url='/accounts/login/')
def get_products():
    products = Product.objects.all().order_by("product_id")
    return products

@user_passes_test(user_group_check, login_url='/accounts/login/')
def create(request):
    # if the request received is POST
    if request.method == 'POST':
        n = request.POST.get('first_name', '')
        a = request.POST.get('address', '')
        num = request.POST.get('contact_number', '')
        home_num = request.POST.get('home_number', '')
        custom = request.POST.get('custom', '')

        # if input is valid, redirect to the furniture choosing page of the invoice just created
        if is_input_valid(n, a, num):
            invoice = Invoice(first_name=n, address=a, contact_number=num, home_number=home_num, sales=request.user.sales)
            date = datetime.now()
            invoice.first_created = date
            invoice.last_update = date
            if custom == 'yes':
                invoice.is_custom_made = True
            invoice.save()
            return HttpResponseRedirect('/invoice/edit/' + str(invoice.invoice_id))
        # else render the page with failure.html
        else:
            return render(request, 'invoice/failure.html', {'error': u'開單失敗!'})

    else:
        return render(request, 'invoice/create.html', {'sales': request.user.sales})

@user_passes_test(user_group_check, login_url='/accounts/login/')
# function for exporting and printing invoice
def print_invoice(request):
    if request.method == 'GET':
        invoice_id = request.GET['invoice']
        if invoice_validation(invoice_id):
            file_name = invoice_id + ".pdf"
            if not settings.DEBUG:
                pdfmetrics.registerFont(TTFont('NewSong', settings.STATIC_ROOT + 'fonts/NewSong.ttf'))
            else:
                pdfmetrics.registerFont(TTFont('NewSong', 'NewSong.ttf'))

            import os
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'private/invoices/'+file_name)

            pdf_creator = PDFCreator(file_path=file_path, font_name='NewSong')
            if pdf_creator.create_invoice(invoice_id):
                subprocess.check_call(['lpr', '-o', 'number-up=2', file_path])
                #subprocess.check_call(['open', file_path])
                return HttpResponseRedirect('/invoice/search/'+invoice_id)

            return render(request, 'invoice/failure.html', {'error': u'列印失敗: 沒有此訂單'})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def print_check_invoice(request):
    file_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".pdf"

    if not settings.DEBUG:
        pdfmetrics.registerFont(TTFont('NewSong', settings.STATIC_ROOT + 'fonts/NewSong.ttf'))
        file_path = settings.MEDIA_ROOT + 'check_invoices/' + file_name
    else:
        pdfmetrics.registerFont(TTFont('NewSong', 'NewSong.ttf'))
        file_path = 'media/check_invoices/' + file_name

    pdf_creator = PDFCreator(file_path=file_path, font_name='NewSong')

    invoices = Invoice.objects.filter(status=Invoice.Waiting, is_custom_made=False)
    custom_invoices = Invoice.objects.filter(status=Invoice.Waiting, is_custom_made=True)

    if pdf_creator.create_check_invoice_list(invoices, custom_invoices):
        subprocess.check_call(['lpr', '-o', 'number-up=2', file_path])
        return render(request, 'invoice/success.html', {})

    return render(request, 'invoice/failure.html', {'error': u'列印失敗: 無法列印對單紙'})


@user_passes_test(user_group_check, login_url='/accounts/login/')
def stats(request, year=-1, month=-1, day=-1):
    if request.method == "GET":
        if year is not -1 and month is not -1 and day is not -1:
            if request.user.is_superuser:
                invoices = Invoice.objects.filter(first_created__year=year, first_created__month=month, first_created__day=day)
            else:
                invoices = Invoice.objects.filter(first_created__year=year, first_created__month=month, first_created__day=day, sales=request.user.sales)
            invoice_count = invoices.count()
            invoices_json = []
            invoice_data = invoices.values()
            for i in range(len(invoices.values())):
                invoices_json.append(invoice_data[i])
            data = {
                'year': year,
                'month': month,
                'day': day,
                'invoices': invoices_json,
            }
            return JsonResponse({'data': data})
        else:
            from calendar import monthrange

            now = datetime.now()
            num_of_days = monthrange(now.year, now.month)[1]
            month = str(now.month) if now.month > 9 else '0{}'.format(now.month)
            first = '{}-{}-01'.format(now.year,month)
            last = '{}-{}-{}'.format(now.year,month,num_of_days)
            invoices = Invoice.objects.filter(sales=request.user.sales, first_created__range=[first, last])
            invoice_count = invoices.count();
            total_amount = 0;
            for invoice in invoices:
                total_amount += invoice.total_amount
            data = {
                'invoice_count': invoice_count,
                'invoice_total_amount': total_amount
            }
            return render(request, 'invoice/stats/index.html', {'data': data})


# method define to return JSON object of products
@user_passes_test(user_group_check, login_url='/accounts/login/')
def get_furniture(request):
    if request.method == "GET":
        search_string = request.GET.get("searchString")
        if search_string:
            try:
                result = Product.objects.all().filter(serial_number__icontains=search_string).order_by("price").values();
            except IndexError:
                return JsonResponse({'error_code': 1})
            else:
                if result:
                    final_result = []
                    # for i in range(result.count()):
                        # temp = {"name": result[i]['name'], 'serial': result[i]['serial_number'], 'price': result[i]['price']}
                        # final_result.append(temp.copy())
                    return JsonResponse({'result': result[:]})
                else:
                    return JsonResponse({'error_code': 2})

        return JsonResponse({'error_code': 2})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def get_invoice_products(request, invoice_id=-1):
    if request.method == "GET":
        if invoice_id is not -1:
            try:
                invoice_products = InvoiceProduct.objects.filter(invoice=Invoice.objects.get(pk=invoice_id));
            except ObjectDoesNotExist:
                return JsonResponse({'error_code': 1})
            else:
                result = []
                for invoice_product in invoice_products:
                    product_dict = model_to_dict(invoice_product.product)
                    invoice_product_dict = model_to_dict(invoice_product)
                    invoice_product_dict.pop('product')
                    invoice_product_dict['product'] = product_dict

                    result.append(invoice_product_dict)

                return JsonResponse({'result': result[:]})

        return JsonResponse({'error_code': 2})

@user_passes_test(user_group_check, login_url='/accounts/login/')
def get_invoice_custom_products(request, invoice_id=-1):
    if request.method == "GET":
        if invoice_id is not -1:
            try:
                result = InvoiceCustomProduct.objects.filter(invoice=Invoice.objects.get(pk=invoice_id)).values();
            except ObjectDoesNotExist:
                return JsonResponse({'error_code': 1})
            else:
                if result:
                    return JsonResponse({'result': result[:]})
                else:
                    return JsonResponse({'error_code': 2})

        return JsonResponse({'error_code': 2})

def tel_validation(num): # check if telephone number has exactly 8 digits
                        # (because Hong Kong uses 8 digits telephone numbers)
    flag = False
    if re.match('^\d{8}$', num):
        # (^ - start of regex) (\d - digits from 0 to 9) ({8} - exactly 8 characters) ($ - end of regex)
        flag = True
    return flag


def address_validation(a): # check if name has more than 0 character and less than or equal to 10 characters
    flag = False
    if 0 < len(a) <= Invoice._meta.get_field('address').max_length:
        flag = True
    return flag


def name_validation(n): # check if name has more than 0 character and less than or equal to 10 characters
    flag = False
    if 0 < len(n) <= Invoice._meta.get_field('first_name').max_length:
        flag = True
    return flag


def invoice_validation(i): # check if invoice id entered has 5 or 6 digits
    flag = False
    if re.match('^\d{5,}$', i):
        flag = True
    return flag


def is_input_valid(n, a, num): # name, address, contact_number
    return name_validation(n) and address_validation(a) and tel_validation(num)
