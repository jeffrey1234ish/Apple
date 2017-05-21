#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class InvoiceQuerySet(models.query.QuerySet):
    def update(self, *args, **kwargs):
        # here queryset update method overridden
        kwargs['last_update'] = timezone.now()
        return super(InvoiceQuerySet, self).update(**kwargs)


class InvoiceManager(models.Manager):
    def get_queryset(self):
        # this is to use your custom queryset methods
        return InvoiceQuerySet(self.model, using=self._db)

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    def __unicode__(self):
        return u'id:{} {}'.format(self.branch_id, self.address)

class Sales(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    sales_name = models.CharField(max_length=30)
    sales_id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, null=True)
    def __unicode__(self):
        return u'{} id:{}'.format(self.sales_name, self.sales_id)

class Invoice(models.Model):
    objects = InvoiceManager()
    first_name = models.CharField(max_length=10)
    #initial = model
    Completed = 'C'
    Uncompleted = 'U'
    Deleted = 'D'
    Waiting = 'W'

    statuses = ((Uncompleted, 'Uncompleted'), (Completed, 'Completed'), (Deleted, 'Deleted'), (Waiting, 'Waiting'))

    Visa = 'V'
    EPS = 'E'
    Cash = 'C'

    payment_types = ((Visa, 'Visa'), (EPS, 'EPS'), (Cash, u'現金'))

    # Primary Data of an Invoice
    invoice_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=8)
    home_number = models.CharField(max_length=8, default='')
    total_amount = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    deposit = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    additional_note = models.CharField(max_length=100, default='')
    is_custom_made = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=1, choices=payment_types, default=Cash)
    # DateTimeFields
    first_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=1, choices=statuses, default=Uncompleted)
    # related_invoice = models.IntegerField(default=0)
    sales = models.ForeignKey(Sales)
    customer = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    # boolean used to indicate whether the invoice is waiting for checking or not

    # drawing = models.ImageField(upload_to='drawing', default='')

    def save(self, *args, **kwargs):
        self.last_update = datetime.now()
        self.remaining = self.total_amount - self.deposit
        return super(Invoice, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{} {}'.format(self.invoice_id, self.first_name)

class ProductAddon(models.Model):
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=20)

class Product(models.Model):
    Red_Cherry = models.BooleanField(default=False)
    Wooden_Black = models.BooleanField(default=False)
    Wooden_White = models.BooleanField(default=False)
    Light_Walnut = models.BooleanField(default=False)
    Maple = models.BooleanField(default=False)
    Oak = models.BooleanField(default=False)
    Glossy_White = models.BooleanField(default=False)
    Black_White = models.BooleanField(default=False)
    Cherry_White = models.BooleanField(default=False)
    Walnut_White = models.BooleanField(default=False)
    Glossy_Champagne = models.BooleanField(default=False)
    Wooden_Champagne = models.BooleanField(default=False)
    
    Other = models.BooleanField(default=True)

    price_multiplies = models.FloatField(default=1.6)
    product_id = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    raw_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    is_wardrobe = models.BooleanField(default=False)
    red_apple = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.raw_price > 0:
            price = int(self.raw_price * self.price_multiplies)
            remainder = price % 10
            if remainder > 4:
                price += 10 - remainder
            else:
                price -= remainder
            self.price = price

        return super(Product, self).save(*args, **kwargs)

    # color = models.

    def __unicode__(self):
        return u'{3} {0} {1} ${2}'.format(self.serial_number, self.description, self.price, self.product_id)

    class Meta:
        ordering = ('serial_number',)

class InvoiceProduct(models.Model):
    Red_Cherry = 'R'
    Wooden_Black = 'B'
    Wooden_White = 'W'
    Light_Walnut = 'L'
    Maple = 'M'
    Oak = "A"
    Glossy_White = 'G'
    Black_White = 'BW'
    Cherry_White = 'CW'
    Walnut_White = 'WW'
    Glossy_Champagne = 'GC'
    Wooden_Champagne = 'C'

    Other = 'O'

    colors = ((Red_Cherry, u'紅櫻桃'), (Wooden_Black, u'黑橡'), (Black_White, u'黑橡/白'), (Cherry_White, u'紅櫻桃/白'),
              (Wooden_White, u'白木紋'), (Light_Walnut, u'淺胡桃'), (Walnut_White, u'淺胡桃/白'), (Glossy_Champagne, u'香檳亮光'),
              (Wooden_Champagne, u'香檳木紋'), (Maple, u'楓木'), (Oak, u'橡木'), (Glossy_White, u'白亮光'), (Other, u'其他'))

    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    side_note = models.CharField(max_length=50, default='')
    color = models.CharField(max_length=2, choices=colors, default=Other)

    def __unicode__(self):
        return u'id:{} {} {} {}'.format(self.id, self.invoice_id, self.product_id, self.quantity)


class InvoiceCustomProduct(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    color = models.CharField(max_length=50, default='')
    side_note = models.CharField(max_length=50, default='')

class InvoiceProductAddon(models.Model):
    invoice_product = models.ForeignKey(InvoiceProduct, on_delete=models.CASCADE)
    product_addon = models.ForeignKey(ProductAddon)
