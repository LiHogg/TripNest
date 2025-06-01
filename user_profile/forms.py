from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Profile, Passport, DriverLicense
from datetime import date
import re

# Валидатор для телефонного номера (валидирует уже отформатированный номер)
phone_validator = RegexValidator(
    regex=r'^\+7 \d{3} \d{3} \d{2}-\d{2}$',
    message='Телефон должен быть в формате +7 123 456 78-90'
)

# === РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ ===
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='E-mail')  # <-- явно EmailField

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    # Дополнительные поля профиля
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    phone_number = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={'placeholder': '+7 123 456 78-90'})
    )
    address = forms.CharField(label='Адрес')
    nationality = forms.CharField(label='Гражданство')
    passport_number = forms.CharField(label='Номер паспорта')
    passport_issue_date = forms.DateField(
        label='Дата выдачи паспорта',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        # 1) проверяем, что только ASCII-символы
        try:
            email.encode('ascii')
        except UnicodeEncodeError:
            raise ValidationError('E-mail должен содержать только латинские буквы и цифры.')
        # 2) дополнительный простой regexp (латиница, цифры и . _ + - перед и после @)
        pattern = r'^[A-Za-z0-9._+-]+@[A-Za-z0-9._+-]+\.[A-Za-z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError('Введите корректный e-mail на латинице, например: user@example.com')
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_passport_number(self):
        number = self.cleaned_data.get('passport_number')
        if Passport.objects.filter(number=number).exists():
            raise ValidationError('Паспорт с таким номером уже зарегистрирован.')
        return number

    def clean_phone_number(self):
        raw = self.cleaned_data.get('phone_number', '')
        digits = re.sub(r'\D', '', raw)
        if digits.startswith('8'):
            digits = '7' + digits[1:]
        if not digits.startswith('7') or len(digits) != 11:
            raise ValidationError('Введите корректный телефонный номер')
        formatted = f"+7 {digits[1:4]} {digits[4:7]} {digits[7:9]}-{digits[9:11]}"
        phone_validator(formatted)
        return formatted

# === РЕДАКТИРОВАНИЕ ПРОФИЛЯ ===
class ProfileEditForm(forms.ModelForm):
    phone_number = forms.CharField(
        label='Телефон',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+7 123 456 78-90'})
    )

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'birth_date', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].required = False
        self.fields['avatar'].required = False

    def clean_phone_number(self):
        raw = self.cleaned_data.get('phone_number', '')
        if not raw:
            return raw
        digits = re.sub(r'\D', '', raw)
        if digits.startswith('8'):
            digits = '7' + digits[1:]
        if not digits.startswith('7') or len(digits) != 11:
            raise ValidationError('Введите корректный телефонный номер')
        formatted = f"+7 {digits[1:4]} {digits[4:7]} {digits[7:9]}-{digits[9:11]}"
        phone_validator(formatted)
        return formatted

# === ПАСПОРТ ===
class PassportForm(forms.ModelForm):
    class Meta:
        model = Passport
        fields = ['number', 'issue_date', 'expiry_date', 'nationality']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            for field in self.fields:
                original_value = getattr(self.instance, field)
                new_value = cleaned_data.get(field)
                if original_value and not new_value:
                    self.add_error(field, 'Нельзя удалять уже заполненное поле.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        for field in ['issue_date', 'expiry_date']:
            if self.instance and getattr(self.instance, field):
                self.initial[field] = getattr(self.instance, field).strftime('%Y-%m-%d')

# === ВОДИТЕЛЬСКОЕ УДОСТОВЕРЕНИЕ ===
class DriverLicenseForm(forms.ModelForm):
    class Meta:
        model = DriverLicense
        fields = ['license_number', 'issue_date', 'expiry_date', 'category']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            for field in self.fields:
                original_value = getattr(self.instance, field)
                new_value = cleaned_data.get(field)
                if original_value and not new_value:
                    self.add_error(field, 'Нельзя удалять уже заполненное поле.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        for field in ['issue_date', 'expiry_date']:
            if self.instance and getattr(self.instance, field):
                self.initial[field] = getattr(self.instance, field).strftime('%Y-%m-%d')

# === БЕЗОПАСНОСТЬ: смена пароля и т.п. ===
class SecurityEditForm(forms.Form):
    current_password = forms.CharField(label='Текущий пароль', widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        if new or confirm:
            if new != confirm:
                raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            for field in self.fields:
                original_value = getattr(self.instance, field)
                new_value = cleaned_data.get(field)
                if original_value and not new_value:
                    self.add_error(field, 'Нельзя удалять уже заполненное поле.')
        return cleaned_data
