from django.db import models

# Create your models here.

class PODProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='pod_products/')
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CustomizedProduct(models.Model):
    base_product = models.ForeignKey(PODProduct, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    custom_image = models.ImageField(upload_to='customized_products/')
    created_at = models.DateTimeField(auto_now_add=True)
