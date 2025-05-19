from django.contrib import admin
from .models import Flight, FlightTicket, TrainTicket, CarReservation, MotoReservation

class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'flight_number',
        'airline',
        'departure_city',
        'arrival_city',
        'departure_date',
        'arrival_date',
        'seats_economy',
        'seats_standard',
        'seats_business',
        'seats_first',
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Только если объект создан впервые (а не редактируется)
        if not change:
            tickets = []
            # Эконом
            for i in range(obj.seats_economy):
                tickets.append(FlightTicket(
                    flight=obj,
                    flight_class='economy',
                    seat_number=f"E{i+1:03d}",
                    price=obj.price_economy if hasattr(obj, 'price_economy') else 0
                ))
            # Стандарт
            for i in range(obj.seats_standard):
                tickets.append(FlightTicket(
                    flight=obj,
                    flight_class='standard',
                    seat_number=f"S{i+1:03d}",
                    price=obj.price_standard if hasattr(obj, 'price_standard') else 0
                ))
            # Бизнес
            for i in range(obj.seats_business):
                tickets.append(FlightTicket(
                    flight=obj,
                    flight_class='business',
                    seat_number=f"B{i+1:03d}",
                    price=obj.price_business if hasattr(obj, 'price_business') else 0
                ))
            # Первый
            for i in range(obj.seats_first):
                tickets.append(FlightTicket(
                    flight=obj,
                    flight_class='first',
                    seat_number=f"F{i+1:03d}",
                    price=obj.price_first if hasattr(obj, 'price_first') else 0
                ))
            FlightTicket.objects.bulk_create(tickets)

admin.site.register(Flight, FlightAdmin)

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
