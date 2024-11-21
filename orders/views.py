from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem, ShippingAddress
from .forms import OrderForm, OrderItemForm, ShippingAddressForm
from products.models import CustomizedProduct

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/list.html', {
        'orders': orders,
        'active_menu': 'orders'
    })

@login_required
@transaction.atomic
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        item_form = OrderItemForm(request.POST)
        
        if order_form.is_valid() and item_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            
            # Calculate total price
            product = item_form.cleaned_data['product']
            quantity = item_form.cleaned_data['quantity']
            order.total_price = product.base_product.price * quantity
            
            order.save()
            
            # Create order item
            order_item = item_form.save(commit=False)
            order_item.order = order
            order_item.price = product.base_product.price * quantity
            order_item.save()
            
            messages.success(request, 'Order created successfully!')
            return redirect('orders:list')
    else:
        order_form = OrderForm()
        item_form = OrderItemForm()
        # Filter products for current user
        item_form.fields['product'].queryset = CustomizedProduct.objects.filter(user=request.user)
        # Filter shipping addresses for current user
        order_form.fields['shipping_address'].queryset = ShippingAddress.objects.filter(user=request.user)

    return render(request, 'orders/create.html', {
        'order_form': order_form,
        'item_form': item_form,
        'active_menu': 'create_order'
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {
        'order': order,
        'active_menu': 'orders'
    })

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('orders:detail', order_id=order.id)

@login_required
def shipping_address_list(request):
    addresses = ShippingAddress.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                ShippingAddress.objects.filter(user=request.user).update(is_default=False)
            address.save()
            messages.success(request, 'Shipping address added successfully!')
            return redirect('orders:shipping_addresses')
    else:
        form = ShippingAddressForm()

    return render(request, 'orders/shipping_addresses.html', {
        'addresses': addresses,
        'form': form,
        'active_menu': 'settings'
    })