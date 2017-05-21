from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    parent_category = models.ForeignKey("ProductCategory", blank=True, null=True)

    def __unicode__(self):
        return u'{0} id:{1}'.format(self.name, self.id)

class Product(models.Model):
    colors = ["Wooden_Black", "Wooden_White", "Light_Walnut", "Maple", "Red_Cherry", "Oak", "Glossy_White"]

    Red_Cherry = models.BooleanField(default=False)
    Wooden_Black = models.BooleanField(default=False)
    Wooden_White = models.BooleanField(default=False)
    Light_Walnut = models.BooleanField(default=False)
    Maple = models.BooleanField(default=False)
    Oak = models.BooleanField(default=False)
    Glossy_White = models.BooleanField(default=False)
    Other = models.BooleanField(default=True)

    product_id = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    height = models.CharField(default="",max_length=10)
    depth = models.CharField(default="",max_length=10)
    width = models.CharField(default="",max_length=10)

    category = models.ForeignKey(ProductCategory, default=None)

    thumbnail = models.ImageField(default=None)
    def __unicode__(self):
        return u'{0}'.format(self.serial_number)

class ProductImages(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField()
