from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'month', 'gender', 'adoption_cost', 'adoption_status', 'location', 'author', 'date_added')
    list_filter = ('gender', 'adoption_status', 'date_added')
    search_fields = ('name', 'author__username', 'location')
    ordering = ('-date_added',)
    readonly_fields = ('date_added',)

    fieldsets = (
        ('Pet Information', {
            'fields': ('name', 'year', 'month', 'gender', 'adoption_cost', 'adoption_status', 'location', 'description')
        }),
        ('Images', {
            'fields': ('image_1', 'image_2', 'image_3', 'image_4')
        }),
        ('Author & Timestamps', {
            'fields': ('author', 'date_added')
        }),
    )
