from django.db import models
from location.models import City

class Excursion(models.Model):
    name = models.CharField('Название экскурсии', max_length=255)
    city = models.ForeignKey(
        City,
        verbose_name='Город',
        on_delete=models.RESTRICT,
        related_name='excursions'
    )
    duration_hours = models.DecimalField(
        'Длительность (часы)',
        max_digits=5,
        decimal_places=2
    )
    price_per_person = models.DecimalField(
        'Цена за человека',
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField('Описание')
    image_url = models.URLField('URL изображения', max_length=255, blank=True, null=True)
    availability_dates = models.TextField(
        'Доступные даты',
        help_text='Перечислите доступные даты через запятую или диапазоны',
        blank=True,
        null=True
    )
    max_participants = models.PositiveIntegerField('Максимальное число участников')
    meeting_point = models.CharField('Место встречи', max_length=255)
    guide_name = models.CharField('Гид', max_length=255)
    language = models.CharField('Язык', max_length=100)
    item_type = models.CharField('Тип услуги', max_length=50)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Экскурсия'
        verbose_name_plural = 'Экскурсии'
        ordering = ['city', 'name']

    def __str__(self):
        return self.name


class ExcursionAvailability(models.Model):
    excursion = models.ForeignKey(
        Excursion,
        verbose_name='Экскурсия',
        on_delete=models.CASCADE,
        related_name='availability'
    )
    available_date = models.DateField('Дата доступности')
    available_slots = models.PositiveIntegerField('Свободных мест')

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Доступность экскурсии'
        verbose_name_plural = 'Доступности экскурсий'
        unique_together = ('excursion', 'available_date')
        ordering = ['available_date']

    def __str__(self):
        return f"{self.excursion.name} — {self.available_date}"
