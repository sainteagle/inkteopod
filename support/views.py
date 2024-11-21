from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, TicketResponse
from .forms import TicketForm, TicketResponseForm

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {
        'tickets': tickets,
        'active_menu': 'support'
    })

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Support ticket created successfully!')
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketForm()
    
    return render(request, 'support/create_ticket.html', {
        'form': form,
        'active_menu': 'support'
    })

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    responses = ticket.responses.all().order_by('created_at')
    
    if request.method == 'POST':
        form = TicketResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ticket = ticket
            response.user = request.user
            response.save()
            messages.success(request, 'Response added successfully!')
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketResponseForm()
    
    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
        'responses': responses,
        'form': form,
        'active_menu': 'support'
    })