from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

def pricing(request):
    return render(request, 'pages/pricing.html')

def terms(request):
    return render(request, 'pages/terms.html')

def privacy(request):
    return render(request, 'pages/privacy.html')

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html', {
        'active_menu': 'dashboard'
    })