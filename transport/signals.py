from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flight, FlightTicket

@receiver(post_save, sender=Flight)
def create_tickets_for_flight(sender, instance, created, **kwargs):
    if created:
        # Автоматически создаём билеты для каждого класса и места
        ticket_data = [
            ('economy', instance.seats_economy, 3000),
            ('standard', instance.seats_standard, 6000),
            ('business', instance.seats_business, 12000),
            ('first', instance.seats_first, 22000),
        ]
        tickets = []
        for flight_class, seat_count, price in ticket_data:
            for seat_number in range(1, seat_count + 1):
                tickets.append(
                    FlightTicket(
                        flight=instance,
                        flight_class=flight_class,
                        seat_number=seat_number,
                        price=price,
                        is_booked=False,
                    )
                )
        if tickets:
            FlightTicket.objects.bulk_create(tickets)
