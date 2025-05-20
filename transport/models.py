from django.db import models
from django.conf import settings
from booking.models import Booking
from user_profile.models import Passport
from location.models import City

class Flight(models.Model):
    flight_number = models.CharField("Номер рейса", max_length=20)
    airline = models.CharField("Авиакомпания", max_length=64)
    departure_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="departure_flights", verbose_name="Откуда")
    arrival_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="arrival_flights",verbose_name="Куда")
    departure_date = models.DateTimeField("Дата и время вылета")
    arrival_date = models.DateTimeField("Дата и время прилета")
    seats_economy = models.PositiveIntegerField("Мест в эконом-классе", default=0)
    seats_standard = models.PositiveIntegerField("Мест в стандарт-классе", default=0)
    seats_business = models.PositiveIntegerField("Мест в бизнес-классе", default=0)
    seats_first = models.PositiveIntegerField("Мест в первом классе", default=0)
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('in_progress', 'Выполняется'),
        ('completed', 'Выполнен'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    def __str__(self):
        return f"{self.flight_number} {self.departure_airport} → {self.arrival_airport}"

class FlightTicket(models.Model):
    FLIGHT_CLASS_CHOICES = [
            ('economy', 'Эконом'),
            ('standard', 'Стандарт'),
            ('business', 'Бизнес'),
            ('first', 'Первый'),
    ]
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.PositiveIntegerField("Место")  # номер места в своём классе
    flight_class = models.CharField("Класс", max_length=10, choices=FLIGHT_CLASS_CHOICES)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    is_booked = models.BooleanField("Забронирован", default=False)
    reserved_until = models.DateTimeField("Временно забронирован до", null=True, blank=True)

    # тут можно добавить связь с бронированием или пользователем (booking, user и т.д.)

    def __str__(self):
        return f"{self.flight.flight_number} | {self.get_flight_class_display()} #{self.seat_number}"

# ---------------------
# Модели для железных дорог
# ---------------------
class Train(models.Model):
    train_number = models.CharField("Номер поезда", max_length=20, unique=True)
    operator = models.CharField("Железнодорожная компания", max_length=64)
    departure_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="departure_trains", verbose_name="Откуда"
    )
    arrival_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="arrival_trains", verbose_name="Куда"
    )
    departure_date = models.DateTimeField("Дата и время отправления")
    arrival_date = models.DateTimeField("Дата и время прибытия")
    duration = models.DurationField("Продолжительность", blank=True, null=True)
    seats_platzkart = models.PositiveIntegerField("Мест в плацкарте", default=0)
    seats_kupe = models.PositiveIntegerField("Мест в купе", default=0)
    seats_sv = models.PositiveIntegerField("Мест в СВ", default=0)
    seats_business = models.PositiveIntegerField("Мест в бизнес-классе", default=0)
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('in_progress', 'В пути'),
        ('completed', 'Выполнен'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def save(self, *args, **kwargs):
        if self.departure_date and self.arrival_date:
            self.duration = self.arrival_date - self.departure_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.train_number} {self.departure_city} → {self.arrival_city}"

class TrainTicket(models.Model):
    TRAIN_CLASS_CHOICES = [
        ('platzkart', 'Плацкарт'),
        ('kupe', 'Купе'),
        ('sv', 'СВ'),
        ('business', 'Бизнес'),
    ]
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name='tickets',
        null=True,
        blank=True
    )
    seat_number = models.PositiveIntegerField(
        "Место",
        default=1,
    )
    train_class = models.CharField(
        "Класс",
        max_length=10,
        choices=TRAIN_CLASS_CHOICES,
        default='platzkart',  # или другой подходящий вариант из TRAIN_CLASS_CHOICES
    )
    price = models.DecimalField(
        "Цена",
        max_digits=8,
        decimal_places=2,
        default=1000.00,
    )
    is_booked = models.BooleanField("Забронирован", default=False)
    reserved_until = models.DateTimeField("Временно забронирован до", null=True, blank=True)

    def __str__(self):
        return f"{self.train.train_number} | {self.get_train_class_display()} #{self.seat_number}"

class TrainedBookingTicket(models.Model):
    # Интеграция с Booking
    id = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='booking_id')
    train_number = models.CharField(max_length=50, blank=True, null=True)
    departure_station = models.CharField(max_length=100, blank=True, null=True)
    arrival_station = models.CharField(max_length=100, blank=True, null=True)
    departure_date = models.DateTimeField(blank=True, null=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    passenger_name = models.CharField(max_length=255, blank=True, null=True)
    passenger_passport = models.ForeignKey(
        Passport,
        on_delete=models.SET_NULL,
        db_column='passenger_passport_id',
        null=True,
        blank=True
    )
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'booking_train_ticket'


class CarReservation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    car_model = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_date = models.DateTimeField(blank=True, null=True)
    dropoff_date = models.DateTimeField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    item_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carreservation'


class MotoReservation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    motorcycle_model = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_date = models.DateTimeField(blank=True, null=True)
    dropoff_date = models.DateTimeField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    item_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'motreservation'


