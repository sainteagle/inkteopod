from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store, StoreProduct, StoreSettings
from .forms import StoreForm, StoreProductForm, StoreSettingsForm
from products.models import CustomizedProduct

@login_required
def store_list(request):
    stores = Store.objects.filter(user=request.user)
    return render(request, 'stores/list.html', {
        'stores': stores,
        'active_menu': 'stores'
    })

@login_required
def create_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.user = request.user
            store.save()
            StoreSettings.objects.create(store=store)
            messages.success(request, 'Store created successfully!')
            return redirect('stores:detail', store_id=store.id)
    else:
        form = StoreForm()
    
    return render(request, 'stores/create.html', {
        'form': form,
        'active_menu': 'stores'
    })

@login_required
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id, user=request.user)
    products = StoreProduct.objects.filter(store=store)
    
    return render(request, 'stores/detail.html', {
        'store': store,
        'products': products,
        'active_menu': 'stores'
    })

@login_required
def add_product(request, store_id):
    store = get_object_or_404(Store, id=store_id, user=request.user)
    
    if request.method == 'POST':
        form = StoreProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, 'Product added to store successfully!')
            return redirect('stores:detail', store_id=store.id)
    else:
        form = StoreProductForm()
        form.fields['product'].queryset = CustomizedProduct.objects.filter(user=request.user)
    
    return render(request, 'stores/add_product.html', {
        'form': form,
        'store': store,
        'active_menu': 'stores'
    })

@login_required
def store_settings(request, store_id):
    store = get_object_or_404(Store, id=store_id, user=request.user)
    settings = store.storesettings
    
    if request.method == 'POST':
        form = StoreSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store settings updated successfully!')
            return redirect('stores:detail', store_id=store.id)
    else:
        form = StoreSettingsForm(instance=settings)
    
    return render(request, 'stores/settings.html', {
        'form': form,
        'store': store,
        'active_menu': 'stores'
    })