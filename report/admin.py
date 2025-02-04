from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'post', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('reporter__username', 'post__name', 'reason', 'admin_feedback')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Report Details', {
            'fields': ('reporter', 'post', 'reason', 'description', 'created_at')
        }),
        ('Admin Review', {
            'fields': ('status', 'admin_feedback')
        }),
    )
