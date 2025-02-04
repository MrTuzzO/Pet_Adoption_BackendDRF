from django.contrib import admin
from .models import Cat, CatColor


@admin.register(CatColor)
class CatColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'adoption_cost', 'adoption_status', 'location', 'is_potty_trained', 'date_added')
    list_filter = ('adoption_status', 'is_potty_trained', 'date_added')
    search_fields = ('name', 'location')
    ordering = ('-date_added',)
    readonly_fields = ('date_added',)

    fieldsets = (
        ('Cat Information', {
            'fields': ('name', 'year', 'month', 'gender', 'adoption_cost', 'adoption_status', 'location', 'food_habit', 'is_potty_trained', 'description')
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
