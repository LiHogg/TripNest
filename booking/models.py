from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room
from excursion.models import Excursion
# Черновик корзины (DraftBooking) — не подтвержденные бронирования (корзина пользователя)
class DraftBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='draft_bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

# Элемент корзины: пока только авиабилеты, но тут могут быть и номера, авто и т.д.
class BookingItem(models.Model):
    draft = models.ForeignKey(DraftBooking, on_delete=models.CASCADE, related_name='items')
    flight_ticket = models.ForeignKey('transport.FlightTicket', null=True, blank=True, on_delete=models.CASCADE)
    hotel_room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)
    excursion = models.ForeignKey(Excursion, null=True, blank=True, on_delete=models.CASCADE)  # 👈
    # Тут позже можно добавить hotel_room, car, excursion и т.д.
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.flight_ticket:
            return f"Авиабилет {self.flight_ticket}"
        # elif self.hotel_room:
        #     return f"Номер {self.hotel_room}"
        # elif self.car:
        #     return f"Авто {self.car}"
        return f"Элемент корзины {self.id}"

# Подтвержденное бронирование (Booking)
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Бронирование #{self.id} пользователя {self.user.username}"

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
