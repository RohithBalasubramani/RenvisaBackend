from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

# import local data
from .serializers import ProductSerializers, OrderSerializers, ReviewSerializers
from .models import Product, Order, Review
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import (
    get_user_model,
)


# create a viewset
class ProductViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Product.objects.all()
    # specify serializer to be used
    serializer_class = ProductSerializers


class OrderViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Order.objects.all()
    # specify serializer to be used
    serializer_class = OrderSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Review.objects.all()
    # specify serializer to be used
    serializer_class = ReviewSerializers

    def create(self, request):
        # Add additional validation or processing.
        data = request.data
        # user = request.user
        print(data)
        product = Product.objects.get(_id=data["product"])
        print(product)

        # Save the post.
        alreadyExists = product.review_set.filter(user=data["user"]).exists()

        if alreadyExists:
            content = {"detail": "Product already reviewed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 2 - No Rating or 0
        elif data["rating"] == 0:
            content = {"detail": "Please select a rating"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 3 - create review
        else:
            review = Review.objects.create(
                user=get_user_model().objects.get(id=data["user"]),
                product=product,
                name=data["name"],
                rating=data["rating"],
                comment=data["comment"],
            )

            reviews = product.review_set.all()
            product.numReviews = len(reviews)

            total = 0
            for i in reviews:
                total += i.rating
            product.rating = total / len(reviews)
            product.save()

        return Response("Review added")


# class MultiImageViewSet(viewsets.ModelViewSet):
#     # define queryset
#     queryset = ProductImages.objects.all()

#     # specify serializer to be used
#     serializer_class = MultiImageSerializers
