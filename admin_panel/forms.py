from django import forms
from location.models import Country, City
from hotel.models import Hotel
from excursion.models import Excursion

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'country']
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'city', 'address', 'rating', 'image']

class ExcursionForm(forms.ModelForm):
    class Meta:
        model = Excursion
        # все поля, нужные для CRUD (без авто-заполняемых created_at/updated_at)
        fields = [
            'name',
            'city',
            'duration_hours',
            'price_per_person',
            'description',
            'image',
            'availability_dates',
            'max_participants',
            'meeting_point',
            'guide_name',
            'language',
            'item_type',
        ]
        widgets = {
            'availability_dates': forms.Textarea(attrs={'rows': 2}),
            'description':      forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'availability_dates': 'Перечислите даты через запятую или диапазоны',
        }
