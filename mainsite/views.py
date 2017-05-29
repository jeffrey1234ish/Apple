#!/usr/bin/env python
# -*- coding: utf-8 -*-
from invoice.models import Product, InvoiceProduct, Invoice

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict

from django.contrib.staticfiles import finders
from django.conf import settings

import urllib2, json, glob, cgi

from django.http import Http404

from models import Product, ProductCategory

from django.contrib.auth.decorators import login_required

def index(request):
    access_token = "1853852278166289|6j122rY62PMpPi1esN_-jgMwAQc"

    try:
        r = json.loads(urllib2.urlopen("https://graph.facebook.com/applefurniturehk/?fields=fan_count&access_token=" + access_token).read())
    except URLError:
        return render(request, 'apple/index.html',{})

    return render(request, 'apple/index.html',{"facebook_count": r['fan_count'], "categorys": ProductCategory.objects.all()})

def landing(request):
    return render(request, 'apple/landing.html', {})

def tinyuen(request):
    splitPath = "invoice"
    paths = glob.glob(finders.find("apple/images/tinyuen")+"/*.*")
    for i in range(len(paths)):
        result = paths[i].split(splitPath)
        if (len(result) == 2):
            paths[i] = result[1]

    return render(request, 'apple/custom.html', {'category_name':u'田園系列', 'paths': paths})

def bedroom(request):
    splitPath = "invoice"
    paths = glob.glob(finders.find("apple/images/bedroom")+"/*.*")
    for i in range(len(paths)):
        result = paths[i].split(splitPath)
        if (len(result) == 2):
            paths[i] = result[1]

    return render(request, 'apple/custom.html', {'category_name':u'睡房系列', 'paths': paths})

def livingroom(request):
    splitPath = "invoice"
    paths = glob.glob(finders.find("apple/images/livingroom")+"/*.*")
    for i in range(len(paths)):
        result = paths[i].split(splitPath)
        if (len(result) == 2):
            paths[i] = result[1]

    return render(request, 'apple/custom.html', {'category_name':u'客廳系列', 'paths': paths})

def studyroom(request):
    splitPath = "invoice"
    paths = glob.glob(finders.find("apple/images/studyroom")+"/*.*")
    for i in range(len(paths)):
        result = paths[i].split(splitPath)
        if (len(result) == 2):
            paths[i] = result[1]

    return render(request, 'apple/custom.html', {'category_name':u'書房系列', 'paths': paths})

def apple(request):
    return render(request, 'apple/apple.html', {})

def category(request, category=None):
    if request.method == "GET":
        if category is not None:
            # handle category detail page
            try:
                cat = ProductCategory.objects.get(pk=category)
            except ProductCategory.DoesNotExist:
                raise Http404("category does not exist")
            except ValueError:
                raise Http404("category does not exist")
            else:
                products = Product.objects.filter(category=cat)

                if cat.parent_category is None:
                    sub_cats = ProductCategory.objects.filter(parent_category=cat)
                    if sub_cats.exists():
                        products = Product.objects.filter(category=cat)
                        return render(request, "apple/product_category.html", {"category": cat, "sub_categories": sub_cats, 'parent_category': cat, 'parent_categories': ProductCategory.objects.filter(parent_category=cat.parent_category)})

                parent_category = ProductCategory.objects.get(pk=cat.parent_category.id)
                parent_categories = ProductCategory.objects.filter(parent_category=parent_category.parent_category)
                sub_categories = ProductCategory.objects.filter(parent_category=parent_category)

                if products.exists():
                    noi = 6
                    nop = (products.count() / (noi + 1)) + 1
                    page = int(request.GET.get("p", 1))

                    first_item = noi*(page-1)
                    last_item = noi*page
                    if page == nop:
                        last_item = products.count()

                    return render(request, "apple/product_category.html", {"products": products[first_item:last_item], 'current_page': page-1, 'pages': range(nop), 'sub_categories': sub_categories, 'parent_categories': parent_categories, 'category': cat, 'parent_category': parent_category})

                return render(request, "apple/product_category.html", {'sub_categories': sub_categories, 'parent_categories': parent_categories, 'category': cat, 'parent_category': parent_category})

def category_main(request):
    if request.method == "GET":
        return HttpResponse("haha")

def product(request, product=None):
    if request.method == "GET":
        if product is not None:
            # handle product detail page
            try:
                p = Product.objects.get(product_id=product)
            except Product.DoesNotExist:
                raise Http404("product does not exist")
            except ValueError:
                return HttpResponse("No product")
            else:
                return render(request, "apple/product_detail.html", {"product": p})
        else:
            raise Http404("page does not exist")


def set_language(request, language):
    from django.utils import translation
    if request.method == 'GET':
        translation.activate(language)
        request.session[translation.LANGUAGE_SESSION_KEY] = language
    return HttpResponseRedirect('/')

@login_required()
def members_page(request):
    invoices = Invoice.objects.filter(customer=request.user)

    return render(request, "apple/members.html", {"invoices": invoices})
