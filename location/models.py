from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)
    has_airport = models.BooleanField("Есть аэропорт", default=False)
    has_train_station = models.BooleanField("Есть ж/д вокзал", default=False)

    def __str__(self):
        return f"{self.name} ({self.country.name})"
