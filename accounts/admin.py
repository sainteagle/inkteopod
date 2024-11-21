from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserRole

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'email_verified', 'is_staff')
    list_filter = ('role', 'email_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'email_verified')}),
    )

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['permissions'].widget = forms.JSONEditor()
        return form

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserRole, UserRoleAdmin)
