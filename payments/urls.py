from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('methods/', views.payment_methods, name='payment_methods'),
    path('process/<int:order_id>/', views.process_payment, name='process_payment'),
]