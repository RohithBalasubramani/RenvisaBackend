from django.shortcuts import render

import jwt

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.urls import reverse

from django.core.mail import send_mail

from django.contrib.auth.hashers import make_password
from django.contrib.auth import (
    get_user_model,
)

# from ecom1App.models import (
#     Product,
#     ProductImages
# )

from ecom1App.serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    UserSerializerWithToken,
    PasswordResetTokenGenerator,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
    # EmailVerificationSerializer,
    # ProductSerializer,
)

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = get_user_model().objects.create_user(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password = data['password']
        )

        serializer = UserSerializerWithToken(user, many=False)

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request=request).domain
        relativeLink = reverse('verify-email')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)

        message = 'Hi ' + user.first_name + 'Use link below to verify your Email Address \n' + absurl
        print(message)

        subject = 'Verify your Email'
        from_email = 'rohithbalasubramani30@gmail.com'
        recipient_list = [user.email, ]
        send_mail( subject, message, from_email, recipient_list, fail_silently = False, )


        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        message = {'detail':'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verifyEmail(request):
    token = request.GET.get('token')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = get_user_model().objects.get(id=payload['user_id'])
        if not user.is_email_verified:
            user.is_email_verified = True
            user.save()
        message = {'detail':'Email successfully verified'}
        return Response(message, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as identifier:
        message = {'detail':'Activation link Expired'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as identifier:
        message = {'detail':'Invalid Token'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    user = get_user_model().objects.all()
    serializer = UserSerializer(user, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def getPasswordResetEmail(request):

    serializer = ResetPasswordEmailRequestSerializer(data=request.data)

    email = request.data['email']

    if get_user_model().objects.filter(email=email).exists():
        user = get_user_model().objects.get(email=email)
        user_id_base64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        #token = RefreshToken.for_user(user)
        current_site = get_current_site(request=request).domain
        relativeLink = reverse('password-reset-confirm', kwargs = {'uidb64':user_id_base64, 'token':token})
        absurl = 'http://' + current_site + relativeLink
        message = 'Hi '+ user.first_name + '\n Use link below to rest your password \n' + absurl
        print(message)
        #data = {'email_body': email_body, 'to_email': user.email, 'email_subject':'Reset your password'}

        subject = 'Reset your password'
        from_email = 'rohithbalasubramani30@gmail.com'
        recipient_list = [user.email, ]
        send_mail( subject, message, from_email, recipient_list, fail_silently = False, )
        #print(email_body)

    return Response({'success': 'we have sent you a link to rest your password'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def passwordTokenCheck(request, uidb64, token):

    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'success': True, 'message': 'Credentials valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

    except DjangoUnicodeDecodeError:
        return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
def setNewPassword(request):

    serializer = SetNewPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'success':True, 'message':'Password reset success'}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def createProduct(request):

#     data = request.data

#     product = Product.objects.create(
#         name = data['name'],
#         referenceNum = data['referenceNum'],
#         brand = data['brand'],
#         actualPrice = data['actualPrice'],
#         sellingPrice=data['sellingPrice'],
#         rating=data['rating']
#     )

#     product.image = request.FILES.get('image')

#     uploaded_images = request.FILES.getlist('uploaded_images')
#     for image in uploaded_images:
#         product_image = ProductImages.objects.create(product=product, image=image)

#     product.save()

#     serializer = ProductSerializer(product, many=False)
#     return Response(serializer.data)

# @api_view(['GET'])
# def listProducts(request):

#     products = Product.objects.all()

#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


