from django.contrib import admin
from .models import Dog


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'breed', 'size', 'adoption_cost', 'adoption_status', 'location', 'date_added')
    list_filter = ('size', 'adoption_status', 'date_added')
    search_fields = ('name', 'breed', 'location')
    ordering = ('-date_added',)
    readonly_fields = ('date_added',)

    fieldsets = (
        ('Dog Information', {
            'fields': ('name', 'year', 'month', 'gender', 'adoption_cost', 'adoption_status', 'location', 'breed', 'size', 'food_habit', 'description')
        }),
        ('Colors', {
            'fields': ('colors',)
        }),
        ('Images', {
            'fields': ('image_1', 'image_2', 'image_3', 'image_4')
        }),
        ('Timestamps', {
            'fields': ('date_added',)
        }),
    )