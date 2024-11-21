from django.contrib import admin
from django.utils.html import format_html
from .models import Deployment

@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'status', 'deployed_by']
    readonly_fields = ['created_at', 'status', 'log', 'deployed_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Yeni kayıt
            obj.deployed_by = request.user
        super().save_model(request, obj, form, change)
