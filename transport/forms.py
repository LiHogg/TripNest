from django import forms
from .models import Flight

from django import forms
from .models import Flight
from location.models import City

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
                attrs={
                    'type': 'datetime-local',  # HTML5! Показывает календарь+время
                    'placeholder': 'Пример: 2025-06-01 12:30',
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'arrival_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder': 'Пример: 2025-06-01 14:30',
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если ввод вручную — подсказываем формат
        self.fields['departure_date'].help_text = "Формат: YYYY-MM-DD HH:MM"
        self.fields['arrival_date'].help_text = "Формат: YYYY-MM-DD HH:MM"
        # Фильтрация городов
        self.fields['departure_city'].queryset = City.objects.filter(has_airport=True)
        self.fields['arrival_city'].queryset = City.objects.filter(has_airport=True)
        # Чтобы значения корректно отображались в datetime-local
        for field in ['departure_date', 'arrival_date']:
            if self.instance and getattr(self.instance, field):
                self.initial[field] = getattr(self.instance, field).strftime('%Y-%m-%dT%H:%M')

