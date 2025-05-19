from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from transport.models import Flight, FlightTicket
from booking.models import BookingItem

class Command(BaseCommand):
    help = 'Удаляет устаревшие брони и обновляет статусы рейсов'

    def handle(self, *args, **options):
        now = timezone.now()

        # Удаление билетов из корзины за 24 часа до вылета
        expired_tickets = FlightTicket.objects.filter(
            is_booked=False,
            flight__departure_date__lte=now + timedelta(hours=24)
        )
        BookingItem.objects.filter(flight_ticket__in=expired_tickets).delete()

        # Обновление статуса рейсов (за 30 секунд до вылета)
        soon_flights = Flight.objects.filter(
            status='scheduled',
            departure_date__lte=now + timedelta(seconds=30)
        )
        soon_flights.update(status='in_progress')

        # Завершение рейсов после прибытия
        completed_flights = Flight.objects.filter(
            status='in_progress',
            arrival_date__lte=now
        )
        completed_flights.update(status='completed')

        self.stdout.write(self.style.SUCCESS("Очистка завершена"))
