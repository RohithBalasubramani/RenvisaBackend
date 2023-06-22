
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from django.contrib.auth import (
    get_user_model,
)
# from ecom1App.models import (
#     Product,
#     ProductImages,
#     ProductSpec,
#     Review
# )

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.urls import reverse

from django.core.mail import send_mail



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for key, value in serializer.items():
            data[key] = value

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields= ['first_name', 'last_name', 'email', 'is_staff']
        read_only_fields = ['id']

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = get_user_model()
        fields= ['first_name', 'last_name', 'email', 'is_staff', 'token']
        read_only_fields = ['id']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        fields = ['token']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields=['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

# class ProductImagesSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductImages
#         fields = ['id', 'product', 'image']

# class ProductSpecSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductSpec
#         fields = '__all__'

# class ReviewSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Review
#         fields  = '__all__'

# class ProductSerializer(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField(read_only=True)
#     specs = serializers.SerializerMethodField(read_only=True)
#     reviews = serializers.SerializerMethodField(read_only=True)
#     # uploaded_images = serializers.ListField(
#     #     child = serializers.ImageField(allow_empty_file=False, use_url=False),
#     #     write_only=True
#     # )
#     class Meta:
#         model=Product
#         fields = '__all__'

#     def get_images(self, obj):
#         images = obj.productimages_set.all()
#         serializer = ProductImagesSerializer(images, many=True)
#         return serializer.data

#     def get_specs(self, obj):
#         specs = obj.productspecs_set.all()
#         serializer = ProductSpecSerializer(specs, many=True)
#         return serializer.data

#     def get_reviews(self, obj):
#         reviews = obj.review_set.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return serializer.data





