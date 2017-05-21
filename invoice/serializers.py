from rest_framework import serializers
from invoice.models import Invoice, InvoiceProduct

class InvoiceProductSerializer(serializers.Serializer):
    class Meta:
        model = InvoiceProduct
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
