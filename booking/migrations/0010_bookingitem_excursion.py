# Generated by Django 5.2.1 on 2025-05-19 22:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_bookingitem_hotel_room'),
        ('excursion', '0002_remove_excursion_image_url_excursion_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingitem',
            name='excursion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='excursion.excursion'),
        ),
    ]
