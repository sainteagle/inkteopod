from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, ShippingAddress

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email']
    inlines = [OrderItemInline]

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'country', 'is_default']
    list_filter = ['is_default', 'country']
    search_fields = ['user__email', 'name', 'city']
