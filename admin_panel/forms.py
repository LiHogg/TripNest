from collections import defaultdict

from django import forms
from django.forms import inlineformset_factory
from location.models import Country, City
from hotel.models import Hotel, RoomClassTemplate
from hotel.forms import RoomClassTemplateForm
from excursion.models import Excursion, ExcursionAvailability
from transport.models import FlightTicket, Flight
from datetime import time
# --------- ГОРОДА И СТРАНЫ ---------
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'country', 'has_airport', 'has_train_station']


# --------- ОТЕЛИ ---------
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name', 'description', 'city', 'address', 'rating', 'price',
            'for_kids', 'image',
            'standard_rooms', 'superior_rooms', 'deluxe_rooms', 'suite_rooms', 'presidential_rooms',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'step': '0.1', 'min': 0, 'max': 5}),
            'price': forms.NumberInput(attrs={'min': 0}),
            'standard_rooms': forms.NumberInput(attrs={'min': 0}),
            'superior_rooms': forms.NumberInput(attrs={'min': 0}),
            'deluxe_rooms': forms.NumberInput(attrs={'min': 0}),
            'suite_rooms': forms.NumberInput(attrs={'min': 0}),
            'presidential_rooms': forms.NumberInput(attrs={'min': 0}),
        }

# Inline formset для описания классов номеров
RoomClassTemplateFormSet = inlineformset_factory(
    parent_model=Hotel,
    model=RoomClassTemplate,
    form=RoomClassTemplateForm,
    extra=5,
    can_delete=True
)


# --------- ЭКСКУРСИИ ---------
class ExcursionForm(forms.ModelForm):
    # Поля для генерации расписания
    start_date = forms.DateField(
        label="Начальная дата",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
    )
    first_start_time = forms.TimeField(
        label="Время начала первой экскурсии",
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False,
        initial=time(10, 0),
    )
    end_date = forms.DateField(
        label="Конечная дата",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
    )

    class Meta:
        model = Excursion
        fields = [
            'name', 'city', 'duration_hours', 'price_per_person',
            'description', 'image', 'max_participants',
            'meeting_point', 'guide_name', 'language', 'item_type',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

ExcursionAvailabilityFormSet = inlineformset_factory(
    Excursion,
    ExcursionAvailability,
    form=forms.modelform_factory(ExcursionAvailability, fields=['available_date', 'start_time', 'available_slots'], widgets={
        'available_date': forms.DateInput(attrs={'type': 'date'}),
        'start_time': forms.TimeInput(attrs={'type': 'time'}),
        'available_slots': forms.NumberInput(attrs={'min': 0}),
    }),
    extra=1,
    can_delete=True
)


# --------- РЕЙСЫ ---------
class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_number', 'airline', 'departure_city', 'arrival_city',
            'departure_date', 'arrival_date',
            'seats_economy', 'seats_standard', 'seats_business', 'seats_first'
        ]
        widgets = {
            'departure_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'arrival_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departure_city'].queryset = City.objects.filter(has_airport=True)
        self.fields['arrival_city'].queryset = City.objects.filter(has_airport=True)
        for field in ['departure_date', 'arrival_date']:
            if self.instance and getattr(self.instance, field):
                self.initial[field] = getattr(self.instance, field).strftime('%Y-%m-%dT%H:%M')


# --------- БИЛЕТЫ ---------
class FlightTicketForm(forms.ModelForm):
    class Meta:
        model = FlightTicket
        fields = '__all__'
