from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('create/', views.create_order, name='create'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel'),
    path('shipping-addresses/', views.shipping_address_list, name='shipping_addresses'),
]