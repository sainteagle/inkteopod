from django.contrib import admin
from .models import Payment, PaymentMethod

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__email', 'order__id', 'transaction_id']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_type', 'last_four', 'is_default', 'created_at']
    list_filter = ['card_type', 'is_default', 'created_at']
    search_fields = ['user__email']