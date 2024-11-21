from django import forms
from .models import GangSheet, GangSheetItem, Module

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'module_type', 'api_key', 'api_secret', 'store_url', 'is_active']
        widgets = {
            'api_secret': forms.PasswordInput(),
        }

class GangSheetForm(forms.ModelForm):
    class Meta:
        model = GangSheet
        fields = ['name', 'width', 'height']

class GangSheetItemForm(forms.ModelForm):
    class Meta:
        model = GangSheetItem
        fields = ['product', 'x_position', 'y_position', 'rotation']