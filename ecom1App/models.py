"""
Database Models.
"""
from django.db import models

from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, blank=False, unique=True)
    phone_number = PhoneNumberField(blank=True, max_length=13)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=200, null=True, blank=True)
    is_business_acc = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class SellerInfo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    company_name = models.CharField(max_length=255)
    seller_type = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)


class BusinessAccInfo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    company_name = models.CharField(max_length=255)
    GST_number = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    position = models.CharField(max_length=255)


# class Product(models.Model):
#     """Product Object"""
#     name = models.CharField(max_length=255)
#     referenceNum = models.CharField(max_length=255)
#     brand = models.CharField(max_length=255)
#     image = models.ImageField(null=True, blank=True, default='/sample.jpg')
#     actualPrice = models.DecimalField(max_digits=9, decimal_places=2)
#     sellingPrice = models.DecimalField(max_digits=9, decimal_places=2)
#     rating = models.DecimalField(max_digits=7, decimal_places=2)
#     numReviews = models.IntegerField(default=0)
#     description = models.TextField(null=True, blank=True)
#     countInStock = models.IntegerField(default=0)
#     category = models.CharField(max_length=200)
#     subCategory = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class ProductImages(models.Model):
#     """Model for multiple image upload"""
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     image = models.ImageField(null=True, blank=True, default='/sample.jpg')

#     def __str__(self):
#         return self.product

# class ProductSpec(models.Model):
#     """Object for product specifications"""
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     specTitle = models.CharField(max_length=200)
#     specDetail = models.CharField(max_length=200)

#     def __str__(self):
#         return self.product

# class Review(models.Model):
#     """Reviews for Products"""
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     reviewTitle = models.CharField(max_length=255)
#     writtenReview = models.TextField(null=True, blank=True)
#     rating = models.IntegerField(default=0)
#     createdAt = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.reviewTitle
