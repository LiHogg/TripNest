from django.db import models
from django.contrib.auth.models import User
from datetime import date


# === ROLE ===
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другое'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')

    # Новое поле для аватара
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # 👇 Установка аватара по умолчанию на основе пола
        if not self.avatar:
            if self.gender == 'male':
                self.avatar = 'avatars/default_male.png'
            elif self.gender == 'female':
                self.avatar = 'avatars/default_female.png'
            else:
                self.avatar = 'avatars/default_neutral.png'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.role}"

    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                        (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

class Passport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passport')
    number = models.CharField(max_length=20)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    nationality = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Passport {self.number} — {self.user.username}"


# === DRIVER LICENSE ===
class DriverLicense(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_license')
    license_number = models.CharField(max_length=20)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    category = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"License {self.license_number} — {self.user.username}"


# === LOGIN HISTORY ===
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    def __str__(self):
        return f"Login {self.login_date} — {self.user.username}"


# === BOOKING HISTORY ===
class History(models.Model):
    TRANSPORT = 'transport'
    HOTEL = 'hotel'
    EXCURSION = 'excursion'

    CATEGORY_CHOICES = [
        (TRANSPORT, 'Транспорт'),
        (HOTEL, 'Отель'),
        (EXCURSION, 'Экскурсия')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    reference_id = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.get_category_display()} — {self.reference_id}"

