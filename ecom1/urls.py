"""ecom1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from ecom1App import views

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/register/', views.registerUser, name='user-register'),
    path('verify-email/', views.verifyEmail, name='verify-email'),
    path('api/users/', views.getUsers, name='users-list'),
    path('api/users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/profile/', views.getUserProfile, name='users-profile'),
    path('request-reset-email/', views.getPasswordResetEmail, name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', views.passwordTokenCheck, name='password-reset-confirm'),
    path('password-reset-complete/', views.setNewPassword, name='password-reset-complete'),
    # path('api/product-create/', views.createProduct, name='product-create'),
    # path('api/product-list/', views.listProducts, name='product-list'),
    path('', include("home.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)