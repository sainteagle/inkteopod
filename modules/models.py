from django.db import models
from django.conf import settings
from products.models import CustomizedProduct

class GangSheet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    width = models.DecimalField(max_digits=10, decimal_places=2)  # in inches
    height = models.DecimalField(max_digits=10, decimal_places=2)  # in inches
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class GangSheetItem(models.Model):
    gangsheet = models.ForeignKey(GangSheet, on_delete=models.CASCADE)
    product = models.ForeignKey(CustomizedProduct, on_delete=models.CASCADE)
    x_position = models.DecimalField(max_digits=10, decimal_places=2)
    y_position = models.DecimalField(max_digits=10, decimal_places=2)
    rotation = models.IntegerField(default=0)  # in degrees

    def __str__(self):
        return f"{self.gangsheet.name} - {self.product.base_product.name}"

class Module(models.Model):
    TYPE_CHOICES = [
        ('shopify', 'Shopify'),
        ('woocommerce', 'WooCommerce'),
        ('etsy', 'Etsy'),
        ('custom', 'Custom Integration')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    module_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    api_key = models.CharField(max_length=200, blank=True)
    api_secret = models.CharField(max_length=200, blank=True)
    store_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.module_type})"
