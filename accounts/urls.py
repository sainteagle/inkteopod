from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    # Ana accounts/ URL'i için yönlendirme
    path('', views.signin, name='account_home'),  # accounts/ direkt olarak signin'e yönlendirilsin
]