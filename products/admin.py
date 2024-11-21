from django.contrib import admin
from django.utils.html import format_html
from .models import PODProduct, CustomizedProduct

@admin.register(PODProduct)
class PODProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

@admin.register(CustomizedProduct)
class CustomizedProductAdmin(admin.ModelAdmin):
    list_display = ['base_product', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'user']
    search_fields = ['base_product__name', 'user__username', 'description']
    ordering = ['-created_at']
