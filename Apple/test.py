from invoice.models import Product
from django.test import TestCase

class ProductTest(TestCase):
    def save_all_product(self):
        for product in Product.objects.all():
            product.save()
