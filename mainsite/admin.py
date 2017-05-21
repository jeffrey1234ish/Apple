from django.contrib import admin

# Register your models here.

from models import ProductCategory, Product

admin.site.register(Product)

from modeltranslation.admin import TranslationAdmin

class ProductCategoryAdmin(TranslationAdmin):
    pass

admin.site.register(ProductCategory, ProductCategoryAdmin)
