# Generated by Django 5.2.1 on 2025-05-26 10:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
        ('location', '0001_initial'),
        ('user_profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarReservation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('car_model', models.CharField(max_length=255)),
                ('pickup_location', models.CharField(max_length=255)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('pickup_date', models.DateTimeField(blank=True, null=True)),
                ('dropoff_date', models.DateTimeField(blank=True, null=True)),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('item_type', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'carreservation',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=20, verbose_name='Номер рейса')),
                ('airline', models.CharField(max_length=64, verbose_name='Авиакомпания')),
                ('departure_date', models.DateTimeField(verbose_name='Дата и время вылета')),
                ('arrival_date', models.DateTimeField(verbose_name='Дата и время прилета')),
                ('seats_economy', models.PositiveIntegerField(default=0, verbose_name='Мест в эконом-классе')),
                ('seats_standard', models.PositiveIntegerField(default=0, verbose_name='Мест в стандарт-классе')),
                ('seats_business', models.PositiveIntegerField(default=0, verbose_name='Мест в бизнес-классе')),
                ('seats_first', models.PositiveIntegerField(default=0, verbose_name='Мест в первом классе')),
                ('status', models.CharField(choices=[('scheduled', 'Запланирован'), ('in_progress', 'Выполняется'), ('completed', 'Выполнен')], default='scheduled', max_length=20)),
                ('arrival_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_flights', to='location.city', verbose_name='Куда')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_flights', to='location.city', verbose_name='Откуда')),
            ],
        ),
        migrations.CreateModel(
            name='FlightTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.PositiveIntegerField(verbose_name='Место')),
                ('flight_class', models.CharField(choices=[('economy', 'Эконом'), ('standard', 'Стандарт'), ('business', 'Бизнес'), ('first', 'Первый')], max_length=10, verbose_name='Класс')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('is_booked', models.BooleanField(default=False, verbose_name='Забронирован')),
                ('reserved_until', models.DateTimeField(blank=True, null=True, verbose_name='Временно забронирован до')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='transport.flight')),
            ],
        ),
        migrations.CreateModel(
            name='MotoReservation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('motorcycle_model', models.CharField(max_length=255)),
                ('pickup_location', models.CharField(max_length=255)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('pickup_date', models.DateTimeField(blank=True, null=True)),
                ('dropoff_date', models.DateTimeField(blank=True, null=True)),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('item_type', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'motreservation',
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_number', models.CharField(max_length=20, unique=True, verbose_name='Номер поезда')),
                ('operator', models.CharField(max_length=64, verbose_name='Железнодорожная компания')),
                ('departure_date', models.DateTimeField(verbose_name='Дата и время отправления')),
                ('arrival_date', models.DateTimeField(verbose_name='Дата и время прибытия')),
                ('duration', models.DurationField(blank=True, null=True, verbose_name='Продолжительность')),
                ('seats_platzkart', models.PositiveIntegerField(default=0, verbose_name='Мест в плацкарте')),
                ('seats_kupe', models.PositiveIntegerField(default=0, verbose_name='Мест в купе')),
                ('seats_sv', models.PositiveIntegerField(default=0, verbose_name='Мест в СВ')),
                ('seats_business', models.PositiveIntegerField(default=0, verbose_name='Мест в бизнес-классе')),
                ('status', models.CharField(choices=[('scheduled', 'Запланирован'), ('in_progress', 'В пути'), ('completed', 'Выполнен')], default='scheduled', max_length=20)),
                ('arrival_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_trains', to='location.city', verbose_name='Куда')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_trains', to='location.city', verbose_name='Откуда')),
            ],
        ),
        migrations.CreateModel(
            name='TrainedBookingTicket',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('train_number', models.CharField(blank=True, max_length=50, null=True)),
                ('departure_station', models.CharField(blank=True, max_length=100, null=True)),
                ('arrival_station', models.CharField(blank=True, max_length=100, null=True)),
                ('departure_date', models.DateTimeField(blank=True, null=True)),
                ('arrival_date', models.DateTimeField(blank=True, null=True)),
                ('passenger_name', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking', models.ForeignKey(db_column='booking_id', on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
                ('passenger_passport', models.ForeignKey(blank=True, db_column='passenger_passport_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_profile.passport')),
            ],
            options={
                'db_table': 'booking_train_ticket',
            },
        ),
        migrations.CreateModel(
            name='TrainTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.PositiveIntegerField(default=1, verbose_name='Место')),
                ('train_class', models.CharField(choices=[('platzkart', 'Плацкарт'), ('kupe', 'Купе'), ('sv', 'СВ'), ('business', 'Бизнес')], default='platzkart', max_length=10, verbose_name='Класс')),
                ('price', models.DecimalField(decimal_places=2, default=1000.0, max_digits=8, verbose_name='Цена')),
                ('is_booked', models.BooleanField(default=False, verbose_name='Забронирован')),
                ('reserved_until', models.DateTimeField(blank=True, null=True, verbose_name='Временно забронирован до')),
                ('train', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='transport.train')),
            ],
        ),
    ]
