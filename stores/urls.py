from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.store_list, name='list'),
    path('create/', views.create_store, name='create'),
    path('<int:store_id>/', views.store_detail, name='detail'),
    path('<int:store_id>/add-product/', views.add_product, name='add_product'),
    path('<int:store_id>/settings/', views.store_settings, name='settings'),
]