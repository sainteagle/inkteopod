from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    path('', views.module_list, name='list'),
    path('create/', views.create_module, name='create'),
    path('gangsheet/', views.gangsheet_builder, name='gangsheet'),
    path('gangsheet/<int:gangsheet_id>/', views.gangsheet_detail, name='gangsheet_detail'),
]