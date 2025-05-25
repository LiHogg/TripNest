from django.db import models
from django.contrib.auth.models import User


class DraftBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DraftBooking {self.id} for {self.user.username}"


class Booking(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Карта'),
        ('cod', 'Наложенный платеж'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Итоговая сумма"
    )
    contact_phone = models.CharField(
        max_length=20,
        verbose_name="Телефон для связи"
    )
    contact_email = models.EmailField(
        verbose_name="Email для связи"
    )
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default='cod',
        verbose_name="Метод оплаты"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="Статус оплаты"
    )

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"


class BookingItem(models.Model):
    draft = models.ForeignKey(
        DraftBooking,
        on_delete=models.CASCADE,
        related_name='items'
    )
    flight_ticket = models.ForeignKey(
        'transport.FlightTicket',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    train_ticket = models.ForeignKey(
        'transport.TrainTicket',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    hotel_room = models.ForeignKey(
        'hotel.Room',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    excursion = models.ForeignKey(
        'excursion.Excursion',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    booking = models.ForeignKey(
        Booking,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='items'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        parts = []
        if self.flight_ticket:
            parts.append(f"FlightTicket {self.flight_ticket.id}")
        if self.train_ticket:
            parts.append(f"TrainTicket {self.train_ticket.id}")
        if self.hotel_room:
            parts.append(f"Room {self.hotel_room.id}")
        if self.excursion:
            parts.append(f"Excursion {self.excursion.id}")
        return f"BookingItem {' | '.join(parts)}"

# Состав бронирования: билеты (аналогично — номера, авто и т.д.)
class BookingTicket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    flight_ticket = models.ForeignKey('transport.FlightTicket', on_delete=models.CASCADE)
    # Можно добавить другие связи по мере расширения функционала

    def __str__(self):
        return f"Билет {self.flight_ticket} в бронировании #{self.booking.id}"

class HotelBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='hotel_bookings')
    hotel_name = models.CharField(max_length=255)
    room_type = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Гостиница: {self.hotel_name} ({self.check_in} – {self.check_out})"


class ExcursionBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='excursion_bookings')
    excursion_title = models.CharField(max_length=255)
    guide_name = models.CharField(max_length=100)
    date = models.DateField()
    people = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Экскурсия: {self.excursion_title} ({self.date})"
