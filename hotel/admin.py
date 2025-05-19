from django.contrib import admin
from .models import Room, Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'rating')
    search_fields = ('name',)
    list_filter = ('city', 'for_kids')
    ordering = ('name',)

    # Поля, которые будут отображаться при создании отеля
    fields = (
        'name', 'description', 'city', 'address', 'rating', 'price',
        'for_kids', 'image',
        'standard_rooms', 'superior_rooms', 'deluxe_rooms', 'suite_rooms', 'presidential_rooms',
    )


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
