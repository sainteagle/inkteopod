from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment, PaymentMethod
from .forms import PaymentMethodForm
from orders.models import Order

@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/list.html', {
        'payments': payments,
        'active_menu': 'payments'
    })

@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payments/detail.html', {
        'payment': payment,
        'active_menu': 'payments'
    })

@login_required
def payment_methods(request):
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            messages.success(request, 'Payment method added successfully!')
            return redirect('payments:payment_methods')
    else:
        form = PaymentMethodForm()
    
    return render(request, 'payments/payment_methods.html', {
        'payment_methods': payment_methods,
        'form': form,
        'active_menu': 'settings'
    })

@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method')
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id, user=request.user)
        
        # Here you would typically integrate with a payment gateway
        # For now, we'll just create a payment record
        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.total_price,
            payment_method='credit_card',
            status='completed',
            transaction_id='dummy-transaction-id'
        )
        
        messages.success(request, 'Payment processed successfully!')
        return redirect('payments:payment_detail', payment_id=payment.id)
    
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    return render(request, 'payments/process_payment.html', {
        'order': order,
        'payment_methods': payment_methods,
        'active_menu': 'payments'
    })