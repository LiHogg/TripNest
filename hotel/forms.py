from django import forms
from .models import Room

from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'hotel',
            'room_class',
            'description',
            'price_per_night',
        ]
        widgets = {
            'room_class': forms.TextInput(attrs={'placeholder': 'Например: Стандарт'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'price_per_night': forms.NumberInput(attrs={'min': 0}),
        }
