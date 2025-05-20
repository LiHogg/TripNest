from django import forms
from .models import Flight, Train, TrainedBookingTicket
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


class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = [
            'train_number',
            'operator',
            'departure_city',
            'arrival_city',
            'departure_date',
            'arrival_date',
            'seats_platzkart',
            'seats_kupe',
            'seats_sv',
            'seats_business',
        ]
        widgets = {
            'departure_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder': 'Напр.: 2025-06-01 12:30',
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'arrival_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder': 'Напр.: 2025-06-01 18:45',
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Help-текст для полей дат
        for fld in ('departure_date', 'arrival_date'):
            self.fields[fld].help_text = "Формат: YYYY-MM-DD HH:MM"
            if self.instance and getattr(self.instance, fld):
                self.initial[fld] = getattr(self.instance, fld).strftime('%Y-%m-%dT%H:%M')

        # Список городов — все города или можно фильтровать по наличию ж/д-станции
        qs = City.objects.all().order_by('name')
        self.fields['departure_city'].queryset = qs
        self.fields['arrival_city'].queryset = qs


class TrainTicketForm(forms.ModelForm):
    class Meta:
        model = TrainedBookingTicket
        # мы не редактируем booking, status, timestamps
        fields = [
            'train_number',
            'departure_station',
            'arrival_station',
            'departure_date',
            'arrival_date',
            'passenger_name',
            'passenger_passport',
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
        # Список паспортов текущего пользователя (если нужно)
        if 'user' in self.initial:
            user = self.initial.pop('user')
            self.fields['passenger_passport'].queryset = user.passports.all()
        # Подсказки по датам
        for fld in ('departure_date', 'arrival_date'):
            self.fields[fld].help_text = "Формат: YYYY-MM-DD HH:MM"
            if self.instance and getattr(self.instance, fld):
                self.initial[fld] = getattr(self.instance, fld).strftime('%Y-%m-%dT%H:%M')