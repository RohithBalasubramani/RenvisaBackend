from django.contrib import admin

"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as translate

from ecom1App import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'first_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            translate('Personal Info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'phone_number'
                )
            }
        ),
        (
            translate('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'is_email_verified',
                    'is_seller',
                    'is_business_acc'
                )
            }
        ),
        (translate('Important dates'), { 'fields' : ('last_login',) })
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields':(
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'phone_number',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_email_verified',
                'is_seller',
                'is_business_acc',
            )
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.SellerInfo)
admin.site.register(models.BusinessAccInfo)
# admin.site.register(models.Product)
# admin.site.register(models.Review)
# admin.site.register(models.ProductImages)
# admin.site.register(models.ProductSpec)
