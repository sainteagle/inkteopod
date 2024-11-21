from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('pod/', views.pod_product_list, name='pod_list'),
    path('my/', views.my_product_list, name='my_list'),
    path('customize/<int:pod_id>/', views.customize_product, name='customize'),
    path('delete/<int:product_id>/', views.delete_product, name='delete'),
]