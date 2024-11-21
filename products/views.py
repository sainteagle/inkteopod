from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PODProduct, CustomizedProduct
from .forms import CustomizedProductForm

@login_required
def pod_product_list(request):
    products = PODProduct.objects.all()
    return render(request, 'products/pod_list.html', {
        'products': products,
        'active_menu': 'pod_products'
    })

@login_required
def my_product_list(request):
    products = CustomizedProduct.objects.filter(user=request.user)
    return render(request, 'products/my_list.html', {
        'products': products,
        'active_menu': 'my_products'
    })

@login_required
def customize_product(request, pod_id):
    pod_product = get_object_or_404(PODProduct, id=pod_id)
    
    if request.method == 'POST':
        form = CustomizedProductForm(request.POST, request.FILES)
        if form.is_valid():
            customized_product = form.save(commit=False)
            customized_product.user = request.user
            customized_product.base_product = pod_product
            customized_product.save()
            messages.success(request, 'Product customized successfully!')
            return redirect('products:my_list')
    else:
        form = CustomizedProductForm()
    
    return render(request, 'products/customize.html', {
        'form': form,
        'pod_product': pod_product,
        'active_menu': 'pod_products'
    })

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(CustomizedProduct, id=product_id, user=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('products:my_list')
