from django.contrib import admin
from .models import Country, City

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name',)
