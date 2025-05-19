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
    created_at = models.DateTimeField(auto_now_add=True)

    # Кол-во номеров по каждому классу
    standard_rooms = models.PositiveIntegerField(default=0)
    superior_rooms = models.PositiveIntegerField(default=0)
    deluxe_rooms = models.PositiveIntegerField(default=0)
    suite_rooms = models.PositiveIntegerField(default=0)
    presidential_rooms = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Room.create_rooms_for_hotel(self)


class Room(models.Model):
    ROOM_CLASSES = [
        ('Standard', 'Standard'),
        ('Superior', 'Superior'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
        ('Presidential Suite', 'Presidential Suite'),
    ]

    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_class = models.CharField(max_length=100, choices=ROOM_CLASSES)
    description = models.TextField(
        verbose_name='Описание',
        help_text='Перечислите удобства через запятую или перенос строки'
    )
    price_per_night = models.PositiveIntegerField(verbose_name='Цена за ночь, ₽')
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.room_class} — {self.hotel.name}'

    @staticmethod
    def create_rooms_for_hotel(hotel):
        base_price = {
            'Standard': 3000,
            'Superior': 4000,
            'Deluxe': 5000,
            'Suite': 7000,
            'Presidential Suite': 10000,
        }

        class_mapping = {
            'Standard': hotel.standard_rooms,
            'Superior': hotel.superior_rooms,
            'Deluxe': hotel.deluxe_rooms,
            'Suite': hotel.suite_rooms,
            'Presidential Suite': hotel.presidential_rooms,
        }

        for room_class, count in class_mapping.items():
            try:
                template = hotel.room_templates.get(room_class=room_class)
            except RoomClassTemplate.DoesNotExist:
                continue  # пропускаем если шаблон не найден

            for _ in range(count):
                Room.objects.create(
                    hotel=hotel,
                    room_class=room_class,
                    description=template.description,
                    price_per_night=base_price[room_class],
                    image=template.image,
                )


class RoomInventory(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='inventory')
    date = models.DateField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'date')

    def __str__(self):
        return f'{self.room} — {self.date} — {"Занято" if self.is_booked else "Свободно"}'


class RoomClassTemplate(models.Model):
    ROOM_CLASSES = Room.ROOM_CLASSES

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_templates')
    room_class = models.CharField(max_length=100, choices=ROOM_CLASSES)
    description = models.TextField()
    image = models.ImageField(upload_to='room_templates/')
    price_per_night = models.PositiveIntegerField(verbose_name='Цена за ночь (₽)')

    class Meta:
        unique_together = ('hotel', 'room_class')

    def __str__(self):
        return f"{self.room_class} — {self.hotel.name}"

