from modeltranslation.translator import translator, TranslationOptions
from mainsite.models import ProductCategory, Product

class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(ProductCategory, ProductCategoryTranslationOptions)

class ProductTranslationOptions(TranslationOptions):
    fields = ('serial_number', 'description',)

translator.register(Product, ProductTranslationOptions)
