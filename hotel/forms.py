from django import forms
from .models import Room, RoomClassTemplate

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'hotel',
            'room_class',
            'description',
            'price_per_night',
            'image',
        ]
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_class': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Перечислите удобства через запятую или перенос строки'
            }),
            'price_per_night': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control',
                'placeholder': 'Цена за ночь в рублях'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class RoomClassTemplateForm(forms.ModelForm):
    class Meta:
        model = RoomClassTemplate
        fields = [
            'room_class',
            'description',
            'image',
            'price_per_night'
        ]
        widgets = {
            'room_class': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Опишите, что входит в номер'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Цена в рублях'
            }),
        }
