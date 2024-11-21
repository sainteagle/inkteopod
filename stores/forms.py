from django import forms
from .models import Store, StoreProduct, StoreSettings

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'logo']

class StoreProductForm(forms.ModelForm):
    class Meta:
        model = StoreProduct
        fields = ['product', 'price', 'is_active']

class StoreSettingsForm(forms.ModelForm):
    class Meta:
        model = StoreSettings
        fields = ['currency', 'theme_color', 'contact_email', 
                 'return_policy', 'shipping_policy']