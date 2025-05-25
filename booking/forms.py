from django import forms

class BookingForm(forms.Form):
    contact_phone = forms.CharField(
        max_length=20,
        label="Телефон для связи",
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (XXX) XXX-XX-XX',
            'class': 'form-control'
        })
    )
    contact_email = forms.EmailField(
        label="Email для связи",
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@example.com',
            'class': 'form-control'
        })
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('card', 'Карта онлайн'),
            ('cod', 'Наложенный платеж')
        ],
        label="Метод оплаты",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
