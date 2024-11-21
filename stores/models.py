from django.db import models
from django.conf import settings
from products.models import CustomizedProduct

class Store(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='store_logos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(CustomizedProduct, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.store.name} - {self.product.base_product.name}"

class StoreSettings(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, default='USD')
    theme_color = models.CharField(max_length=7, default='#4F46E5')  # Hex color
    contact_email = models.EmailField()
    return_policy = models.TextField(blank=True)
    shipping_policy = models.TextField(blank=True)