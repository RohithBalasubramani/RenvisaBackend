# from django import forms
# from django.forms.widgets import ClearableFileInput
# from .models import Product

# class MultiImageField(forms.MultiValueField):
#     widget = forms.FileInput(attrs={'multiple': True})

#     def __init__(self, *args, **kwargs):
#         fields = [forms.ImageField() for i in range(4)]  # Set the number of fields as per your requirement
#         super().__init__(fields, *args, **kwargs)

#     def compress(self, data_list):
#         return data_list

# class MyModelForm(forms.ModelForm):
#     images = MultiImageField(required=False)

#     class Meta:
#         model = Product
#         fields = ('title', 'description', 'images')
