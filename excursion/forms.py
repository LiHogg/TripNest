from django import forms
from .models import Excursion, ExcursionAvailability
from django.forms.models import inlineformset_factory

class ExcursionForm(forms.ModelForm):
    class Meta:
        model = Excursion
        fields = [
            'name',
            'city',
            'duration_hours',
            'price_per_person',
            'max_participants',
            'meeting_point',
            'guide_name',
            'language',
            'item_type',
            'description',
            'image',
            'availability_dates',
        ]
        widgets = {
            'description':   forms.Textarea(attrs={'rows': 4}),
            'availability_dates': forms.Textarea(attrs={'rows': 2, 'placeholder': 'YYYY-MM-DD, или диапазон 2025-06-01—2025-06-10'}),
            'image_url':     forms.URLInput(attrs={'placeholder': 'https://...'}),
            'meeting_point': forms.TextInput(attrs={'placeholder': 'Например: пл. Революции, 1'}),
        }

class ExcursionAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ExcursionAvailability
        fields = ['available_date', 'available_slots']
        widgets = {
            'available_date':  forms.DateInput(attrs={'type': 'date'}),
            'available_slots': forms.NumberInput(attrs={'min': 0}),
        }

# FormSet для работы с множеством дат доступности прямо внутри формы экскурсии
ExcursionAvailabilityFormSet = inlineformset_factory(
    Excursion,
    ExcursionAvailability,
    form=ExcursionAvailabilityForm,
    extra=1,    # сколько дополнительных пустых строк добавить
    can_delete=True
)
