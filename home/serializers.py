from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order, Review


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


# class MultiImageSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImages
#         fields = "__all__"
