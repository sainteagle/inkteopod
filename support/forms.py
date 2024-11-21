from django import forms
from .models import Ticket, TicketResponse

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'priority']

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        fields = ['message']