from django.core.management.base import BaseCommand
from transport.models import Flight
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Обновляет статус рейсов в зависимости от времени вылета'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Вылет уже прошёл (например, завершён через 2 часа после вылета)
        Flight.objects.filter(
            departure_date__lte=now - timedelta(hours=2),
        ).update(status='completed')

        # Вылет начинается прямо сейчас (в пределах ±1 минуты)
        Flight.objects.filter(
            departure_date__lte=now,
            departure_date__gte=now - timedelta(minutes=1),
        ).update(status='in_progress')

        # Вылет ещё впереди
        Flight.objects.filter(
            departure_date__gt=now
        ).update(status='scheduled')

        self.stdout.write("Статусы рейсов обновлены.")
