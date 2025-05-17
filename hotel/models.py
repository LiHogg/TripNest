from django.db import models
from location.models import City

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    rating = models.FloatField()
    price = models.PositiveIntegerField(default=0)
    for_kids = models.BooleanField(default=False)
    image = models.ImageField(upload_to='hotel_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # ← если ты хочешь показывать дату

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        related_name='rooms',
        on_delete=models.CASCADE
    )
    # теперь просто текстовое поле, в котором вы вписываете класс номера вручную
    room_class = models.CharField(
        max_length=100,
        verbose_name='Класс номера'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Перечислите удобства через запятую или перенос строки'
    )
    price_per_night = models.PositiveIntegerField(
        verbose_name='Цена за ночь, ₽'
    )

    def __str__(self):
        return f'{self.room_class} — {self.hotel.name}'