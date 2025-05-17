from django.contrib import admin
from .models import Room, Hotel

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'rating')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'hotel',
        'room_class',
        'price_per_night',
    )
    list_filter = ('hotel', 'room_class')
    search_fields = ('room_class', 'hotel__name')
    ordering = ('hotel', 'room_class')
