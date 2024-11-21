from django import forms
from .models import Order, OrderItem, ShippingAddress

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'address_line1', 'address_line2', 'city', 
                 'state', 'postal_code', 'country', 'is_default']