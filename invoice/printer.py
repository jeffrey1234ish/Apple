#!/usr/bin/env python
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4, A5, landscape
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from models import InvoiceProduct, Invoice, Product, InvoiceCustomProduct
from django.conf import settings
from reportlab.pdfgen import canvas
import cgi

class MyParagraph(Paragraph):
    def drawOn(self, canv, x, y, _sW=0):
        canv.saveState()
        canv.setStrokeColor((1, 0, 0))
        canv.setLineWidth(1)
        print 'x=%s y=%s width=%s height=%s' % (x, y, self.width, self.height)
        canv.rect(x, y, self.width, self.height, stroke=1, fill=0)
        canv.restoreState()
        Paragraph.drawOn(self, canv, x, y, _sW)

class PDFCreator(object):
    def __init__(self, file_path='', font_name=''):
        self.file_path = file_path
        self.font_name = font_name

    def set_file_path(self, file_path):
        self.file_path = file_path

    def create_check_invoice_list(self, invoices, custom_invoices):
        if self.file_path == '' and self.font_name == '':
            return False

        width, height = A4

        element = []
        try:
            invoice_pdf = SimpleDocTemplate(self.file_path, pagesize=A5,
                                        rightMargin=50, leftMargin=50,
                                        topMargin=50, bottomMargin=18)
        except:
            return False
        else:
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='invoice', fontName=self.font_name, fontSize=12))
            styles.add(ParagraphStyle(name='invoice2', fontName=self.font_name, fontSize=12, spaceBefore=5.83 * inch))

            invoice_pdf.build(element)

            return True



    # return False if unable to create invoice
    # return True if pdf is created successfully
    def create_invoice(self, invoice_id=-1):
        if self.file_path == '' and self.font_name == '':
            return False

        width, height = A4

        def coord(x, y, unit=1):
            x, y = x * unit, height - y * unit

            print('{} {}'.format(x, y))

            return x, y

        invoice = Invoice.objects.get(pk=invoice_id)
        invoice_products = InvoiceProduct.objects.filter(invoice=invoice)
        invoice_custom_products = InvoiceCustomProduct.objects.filter(invoice=invoice)

        products = []
        element = []

        try:
            can = canvas.Canvas(self.file_path, pagesize=A4)
        except:
            return False
        else:
            fontSize = 15

            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='invoice', fontName=self.font_name, fontSize=fontSize))
            styles.add(ParagraphStyle(name='right-invoice', fontName=self.font_name, fontSize=fontSize))

            page_number = 1

            offset_y = 10

            max_number = 5
            j = 0

            for product in invoice_products:
                temp_product = {}
                temp_product['serial_number'] = product.product.serial_number
                temp_product['color'] = product.get_color_display()
                temp_product['side_note'] = cgi.escape(product.side_note)
                temp_product['quantity'] = product.quantity
                temp_product['price'] = product.product.price
                products.append(temp_product)

            for product in invoice_custom_products:
                temp_product = {}
                temp_product['serial_number'] = product.name
                temp_product['color'] = product.color
                temp_product['side_note'] = product.side_note
                temp_product['quantity'] = product.quantity
                temp_product['price'] = product.price
                products.append(temp_product)

            number_of_page = (len(products) / (max_number + 1)) + 1
            last_index = 0
            for i in range(number_of_page):
                offset_x = 0
                for k in range(2):
                    product_offset = 0

                    ptext = u'{}'.format(invoice.first_name)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(33 + offset_x,49 + offset_y,mm))

                    ptext = u'{} / {}'.format(invoice.contact_number, invoice.home_number)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(33 + offset_x,59 + offset_y,mm))

                    ptext = u'{}'.format(invoice.address)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(20 + offset_x, 76 + offset_y, mm))

                    ptext = u'{}'.format(invoice.first_created.date())
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(153 + offset_x, 49 + offset_y, mm))

                    ptext = u'{}'.format(invoice_id)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(153 + offset_x, 59 + offset_y, mm))

                    ptext = u'{}/{}'.format(page_number, number_of_page)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(153 + offset_x, 68 + offset_y, mm))

                    ptext = u'{}'.format(invoice.additional_note)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(10 + offset_x, 255 + offset_y, mm))

                    ptext = u'${}'.format(invoice.total_amount)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(180 + offset_x, 225 + offset_y, mm))

                    ptext = u'${}'.format((invoice.deposit + invoice.discount))
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(180 + offset_x, 236 + offset_y, mm))

                    ptext = u'{}'.format(invoice.get_payment_type_display())
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(180 + offset_x, 247 + offset_y, mm))

                    ptext = u'${}'.format(invoice.remaining)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(180 + offset_x, 258 + offset_y, mm))

                    ptext = u'{}'.format(invoice.sales.sales_name)
                    p = Paragraph(ptext, styles["invoice"])
                    p.wrapOn(can, width, height)
                    p.drawOn(can, *coord(5 + offset_x, 285 + offset_y, mm))

                    j = 0
                    while j < max_number and (j+last_index) < len(products):
                        ptext = u'{}'.format(products[j + last_index]['serial_number'])
                        p = Paragraph(ptext, styles["invoice"])
                        p.wrapOn(can, width, height)
                        p.drawOn(can, *coord(15 + offset_x, 104+product_offset + offset_y, mm))

                        ptext = u'{}'.format(products[j + last_index]['color'])
                        p = Paragraph(ptext, styles["invoice"])
                        p.wrapOn(can, width, height)
                        p.drawOn(can, *coord(15 + offset_x, 110+product_offset + offset_y, mm))

                        ptext = u'{}'.format(products[j + last_index]['side_note'])
                        p = Paragraph(ptext, styles["invoice"])
                        p.wrapOn(can, width, height)
                        p.drawOn(can, *coord(15 + offset_x, 116+product_offset + offset_y, mm))

                        ptext = u'{}'.format(products[j + last_index]['quantity'])
                        p = Paragraph(ptext, styles["invoice"])
                        p.wrapOn(can, width, height)
                        p.drawOn(can, *coord(140 + offset_x, 104+product_offset + offset_y, mm))

                        ptext = u'${}'.format(products[j + last_index]['price'])
                        p = Paragraph(ptext, styles["invoice"])
                        p.wrapOn(can, width, height)
                        p.drawOn(can, *coord(170 + offset_x, 104+product_offset + offset_y, mm))

                        product_offset += 22

                        j += 1

                    offset_x = offset_x + 8
                    can.showPage()
                last_index += j
                page_number += 1
            can.save()

            return True

    def other(self):
        products = []
        invoice_id = 0; fontSize = 20
        element = []
        name = 0; address = 0; num = 0
        invoice_pdf = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='invoice', fontName=self.font_name, fontSize=fontSize))
        styles.add(ParagraphStyle(name='right-invoice', fontName=self.font_name, fontSize=fontSize))

        ptext = u'<para alignment="right">訂單編號 {}</para>'.format(invoice_id)
        p = Paragraph(ptext, styles["invoice"])
        p.drawOn
        element.append(p)
        element.append(Spacer(1, fontSize))

        ptext = u'{}'.format(name)
        element.append(Paragraph(ptext, styles["invoice"]))
        element.append(Spacer(1, fontSize))

        ptext = u'{}'.format(address)
        element.append(Paragraph(ptext, styles["invoice"]))
        element.append(Spacer(1, fontSize))

        ptext = u'電話:{}'.format(num)
        element.append(Paragraph(ptext, styles["invoice"]))
        element.append(Spacer(1, 50))

        for i in range(len(products)):
            product = products[i]
            ptext = u'{}    {}    {}    {}'.format(product["product_serial"], product["side_note"],
                                                   product["quantity"], convert_color_to_chinese(product["color"]))
            element.append(Paragraph(ptext, styles["invoice"]))
            element.append(Spacer(1, 12))

        invoice_pdf.build(element)
