from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.JSONField(default=dict)  # Sayfa ve menü izinleri
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)
    email_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
