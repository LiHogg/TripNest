from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from datetime import date

from .models import Profile, Role, Passport, DriverLicense, LoginHistory
from .forms import (
    ProfileEditForm, UserRegistrationForm, SecurityEditForm,
    PassportForm, DriverLicenseForm, UserEditForm
)

def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    passports = Passport.objects.filter(user=request.user)
    driver_licenses = DriverLicense.objects.filter(user=request.user)
    login_history = LoginHistory.objects.filter(user=request.user).order_by('-login_date')[:5]

    return render(request, 'user_profile/profile.html', {
        'profile': profile,
        'passports': passports,
        'driver_licenses': driver_licenses,
        'login_history': login_history,
    })

def edit_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    passport = Passport.objects.filter(user=request.user).first()
    license = DriverLicense.objects.filter(user=request.user).first()
    user_form = UserEditForm(request.POST or None, instance=request.user)
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=profile)
    passport_form = PassportForm(request.POST or None, instance=passport, prefix='passport')
    license_form = DriverLicenseForm(request.POST or None, instance=license, prefix='license')
    security_form = SecurityEditForm(request.POST or None)

    if request.method == 'POST':
        all_valid = all([
            profile_form.is_valid(),
            passport_form.is_valid(),
            license_form.is_valid(),
            security_form.is_valid(),
            user_form.is_valid()
        ])

        if all_valid:
            profile_form.save()
            user_form.save()

            # Обработка паспорта
            passport_obj = passport_form.save(commit=False)
            if any(passport_form.cleaned_data.get(field) for field in passport_form.fields):
                passport_obj.user = request.user
                # если форма не дала новую дату выдачи — оставляем старую
                if passport_obj.issue_date is None and passport:
                    passport_obj.issue_date = passport.issue_date
                # гарантируем, что expiry_date не будет NULL
                if passport_obj.expiry_date is None:
                    if passport:
                        passport_obj.expiry_date = passport.expiry_date
                    else:
                        # новый паспорт: expiry_date = issue_date + 10 лет
                        passport_obj.expiry_date = passport_obj.issue_date.replace(
                            year=passport_obj.issue_date.year + 10
                        )
                passport_obj.save()

            # Обработка водительского удостоверения
            license_obj = license_form.save(commit=False)
            if any(license_form.cleaned_data.get(field) for field in license_form.fields):
                license_obj.user = request.user
                license_obj.save()

            return redirect('profile')

    return render(request, 'user_profile/edit_profile.html', {
        'form': profile_form,
        'passport_form': passport_form,
        'license_form': license_form,
        'security_form': security_form,
        'user_form': user_form,
    })


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(form.cleaned_data['password'])
            user.save()

            role, _ = Role.objects.get_or_create(name='user')

            Profile.object.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                addres=form.cleaned_data['addres'],
                role=role
            )

            issue_date = form.cleaned_data('passport_issue_date')
            expiry_date = issue_date.replace(year=issue_date.year + 10)
            Passport.object.create(
                user=user,
                number=form.cleaned_data['passport_number'],
                issue_date=issue_date,
                expiry_date=expiry_date,
                nationality=form.cleaned_data['nationality']
            )

            return redirect(reverse('home'))
    else:
        form = UserRegistrationForm()

    return render(request, 'user_profile/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if getattr(user.profile.role, 'name', None) == 'admin':
                return redirect('dashboard')
            else:
                return redirect('home_user')
    else:
        form = AuthenticationForm()

    return render(request, 'user_profile/login.html', {'form': form})

def profile_details_view(request):
    profile = Profile.objects.filter(user=request.user).first()
    passport = Passport.objects.filter(user=request.user).first()
    license = DriverLicense.objects.filter(user=request.user).first()

    return render(request, 'user_profile/profile_details.html', {
        'user': request.user,
        'profile': profile,
        'passport': passport,
        'license': license,
    })