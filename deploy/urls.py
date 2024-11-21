from django.urls import path
from . import views

app_name = 'deploy'

urlpatterns = [
    path('deployment/<int:deployment_id>/deploy/', 
         views.trigger_deployment, 
         name='trigger_deployment'),
]
