# Generated by Django 5.2.1 on 2025-05-26 10:32

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Excursion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название экскурсии')),
                ('duration_hours', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Длительность (часы)')),
                ('price_per_person', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за человека')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='excursions/', verbose_name='Изображение')),
                ('availability_dates', models.TextField(blank=True, help_text='Перечислите доступные даты через запятую или диапазоны', null=True, verbose_name='Доступные даты')),
                ('max_participants', models.PositiveIntegerField(verbose_name='Максимальное число участников')),
                ('meeting_point', models.CharField(max_length=255, verbose_name='Место встречи')),
                ('guide_name', models.CharField(max_length=255, verbose_name='Гид')),
                ('language', models.CharField(max_length=100, verbose_name='Язык')),
                ('item_type', models.CharField(max_length=50, verbose_name='Тип услуги')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='excursions', to='location.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Экскурсия',
                'verbose_name_plural': 'Экскурсии',
                'ordering': ['city', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ExcursionAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_date', models.DateField(verbose_name='Дата доступности')),
                ('available_slots', models.PositiveIntegerField(verbose_name='Свободных мест')),
                ('start_time', models.TimeField(default=datetime.time(10, 0))),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('excursion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability', to='excursion.excursion', verbose_name='Экскурсия')),
            ],
            options={
                'verbose_name': 'Доступность экскурсии',
                'verbose_name_plural': 'Доступности экскурсий',
                'ordering': ['available_date'],
                'unique_together': {('excursion', 'available_date', 'start_time')},
            },
        ),
    ]
