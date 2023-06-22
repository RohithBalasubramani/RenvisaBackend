from django.urls import include, path

# import routers
from rest_framework import routers

# import everything from views
from .views import *

# define the router
router = routers.DefaultRouter()

# define the router path and viewset to be used
router.register(r"product", ProductViewSet)
router.register(r"order", OrderViewSet)
router.register(r"review", ReviewViewSet)

# router.register(r'images', MultiImageViewSet)

# specify URL Path for rest_framework
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
