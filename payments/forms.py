from django import forms
from .models import PaymentMethod

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['card_type', 'last_four', 'expiry_month', 'expiry_year', 'is_default']