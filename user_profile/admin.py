from django.contrib import admin
from .models import (
    Profile, Role, Passport, DriverLicense, LoginHistory, History
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'birth_date', 'role')
    search_fields = ('user__username', 'phone_number', 'address')
    list_filter = ('role', 'birth_date')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'issue_date', 'expiry_date', 'nationality')
    search_fields = ('number', 'user__username')
    list_filter = ('nationality',)


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'issue_date', 'expiry_date', 'category')
    search_fields = ('license_number', 'user__username')
    list_filter = ('category',)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_date', 'ip_address')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('login_date',)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'reference_id', 'date', 'status')
    search_fields = ('user__username', 'category', 'reference_id')
    list_filter = ('category', 'status')
