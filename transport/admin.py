from django.contrib import admin
from .models import Flight, FlightTicket, TrainTicket, CarReservation, MotoReservation

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'flight_number', 'airline',
        'departure_city', 'arrival_city',
        'departure_date', 'arrival_date',
        'seats_economy', 'seats_standard', 'seats_business', 'seats_first'
    )
    search_fields = ('flight_number', 'airline', 'departure_airport', 'arrival_airport')
    list_filter = ('airline',)

@admin.register(FlightTicket)
class FlightTicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'flight', 'flight_class', 'seat_number', 'price', 'is_booked'
    )
    search_fields = ('flight__flight_number',)
    list_filter = ('flight_class', 'is_booked', 'flight')

@admin.register(TrainTicket)
class TrainTicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'train_number', 'departure_station', 'arrival_station', 'departure_date'
    )
    search_fields = ('train_number', 'departure_station', 'arrival_station')
    list_filter = ('train_number',)

@admin.register(CarReservation)
class CarReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'car_model', 'pickup_location', 'pickup_date', 'total_cost'
    )
    search_fields = ('car_model', 'user__username')
    list_filter = ('pickup_location',)

@admin.register(MotoReservation)
class MotoReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'motorcycle_model', 'pickup_location', 'pickup_date', 'total_cost'
    )
    search_fields = ('motorcycle_model', 'user__username')
    list_filter = ('pickup_location',)
