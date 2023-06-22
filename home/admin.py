from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from .models import *

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ("name", "brand", "reference_number", "discounted_price")
    ordering = ("discounted_price",)
    search_fields = ("name", "brand")
    exclude = ("rating", "numReviews")


admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
# admin.site.register(ProductImages)
