from django.contrib import admin
from .models import Excursion, ExcursionAvailability

@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'city',
        'duration_hours',
        'price_per_person',
        'language',
        'guide_name',
    )
    list_filter = (
        'city',
        'language',
    )
    search_fields = (
        'name',
        'description',
        'guide_name',
    )
    ordering = ('city', 'name')
    fieldsets = (
        (None, {
            'fields': ('name', 'city', 'item_type')
        }),
        ('Детали', {
            'fields': (
                'duration_hours',
                'price_per_person',
                'max_participants',
                'language',
                'guide_name',
                'meeting_point',
            )
        }),
        ('Контент', {
             'fields': ('description', 'image', 'availability_dates')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ExcursionAvailability)
class ExcursionAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'excursion',
        'available_date',
        'available_slots',
    )
    list_filter = (
        'available_date',
        'excursion__city',
    )
    search_fields = (
        'excursion__name',
    )
    date_hierarchy = 'available_date'
    ordering = ('available_date',)
