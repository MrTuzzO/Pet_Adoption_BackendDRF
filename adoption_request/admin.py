from django.contrib import admin
from .models import AdoptionRequest


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'requester', 'status', 'date_requested', 'date_updated')
    list_filter = ('status', 'date_requested')
    search_fields = ('pet__name', 'requester__username', 'requester__email')
    ordering = ('-date_requested',)
    readonly_fields = ('date_requested', 'date_updated')

    fieldsets = (
        ('Adoption Details', {
            'fields': ('pet', 'requester', 'status')
        }),
        ('Contact Information', {
            'fields': ('use_default_info', 'contact_info', 'message')
        }),
        ('Timestamps', {
            'fields': ('date_requested', 'date_updated')
        }),
    )
