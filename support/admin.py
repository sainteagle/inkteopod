from django.contrib import admin
from .models import Ticket, TicketResponse

class TicketResponseInline(admin.TabularInline):
    model = TicketResponse
    extra = 0

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'user', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['subject', 'description', 'user__email']
    inlines = [TicketResponseInline]

@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['message', 'user__email']