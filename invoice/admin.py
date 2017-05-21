from django.contrib import admin

# Register your models here.

from invoice.models import Product, Invoice, InvoiceProduct, InvoiceCustomProduct, Sales, Branch

def make_is_wardrobe(modeladmin, request, queryset):
    queryset.update(is_wardrobe=True)
make_is_wardrobe.short_description = "Mark selected products as wardrobe"

class ProductAdmin(admin.ModelAdmin):
    actions = [make_is_wardrobe]

admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice)
admin.site.register(InvoiceProduct)
admin.site.register(InvoiceCustomProduct)
admin.site.register(Sales)
admin.site.register(Branch)
