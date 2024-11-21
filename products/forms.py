from django import forms
from .models import CustomizedProduct

class CustomizedProductForm(forms.ModelForm):
    class Meta:
        model = CustomizedProduct
        fields = ['custom_image', 'description']