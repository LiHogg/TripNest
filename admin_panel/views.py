from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    CountryForm, CityForm, HotelForm,
    ExcursionForm, ExcursionAvailabilityFormSet,
    RoomClassTemplateFormSet, FlightForm, TrainForm
)
from hotel.forms import RoomForm
from user_profile.models import Profile, Passport, DriverLicense, LoginHistory, History
from location.models import Country, City
from hotel.models import Hotel, Room
from excursion.models import Excursion
from excursion.utils import generate_excursion_schedule
from transport.models import Flight, Train
from django.contrib.auth.models import User
from transport.views import create_tickets_for_train
# === DASHBOARD ===
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

# === USER CRUD ===
def user_list(request):
    users = User.objects.all().select_related('profile', 'passport', 'driver_license')
    return render(request, 'admin_panel/user_list.html', {'users': users})

def user_edit(request, id):
    user = get_object_or_404(User, id=id)
    profile = getattr(user, 'profile', None)
    passport = getattr(user, 'passport', None)
    license = getattr(user, 'driver_license', None)
    history = History.objects.filter(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        if profile:
            profile.phone_number = request.POST.get('phone_number')
            profile.address = request.POST.get('address')
            profile.birth_date = request.POST.get('birth_date')
            profile.save()
        return redirect('admin_panel:user_list')

    return render(request, 'admin_panel/user_edit.html', {
        'user': user,
        'profile': profile,
        'passport': passport,
        'license': license,
        'history': history,
    })

def user_deactivate(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = False
    user.save()
    return redirect('admin_panel:user_list')

def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('admin_panel:user_list')

# === COUNTRY CRUD ===
def country_list(request):
    countries = Country.objects.all()
    return render(request, 'admin_panel/country_list.html', {'countries': countries})

def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:country_list')
    else:
        form = CountryForm()
    return render(request, 'admin_panel/country_form.html', {'form': form, 'title': 'Добавить страну'})

def country_edit(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:country_list')
    else:
        form = CountryForm(instance=country)
    return render(request, 'admin_panel/country_form.html', {'form': form, 'title': 'Редактировать страну'})

def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    return redirect('admin_panel:country_list')

# === CITY CRUD ===
def city_list(request):
    cities = City.objects.select_related('country').all()
    return render(request, 'admin_panel/city_list.html', {'cities': cities})

def city_create(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:city_list')
    else:
        form = CityForm()
    return render(request, 'admin_panel/city_form.html', {'form': form, 'title': 'Добавить город'})

def city_edit(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:city_list')
    else:
        form = CityForm(instance=city)
    return render(request, 'admin_panel/city_form.html', {'form': form, 'title': 'Редактировать город'})

def city_delete(request, pk):
    city = get_object_or_404(City, pk=pk)
    city.delete()
    return redirect('admin_panel:city_list')


# === HOTEL CRUD ===
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'admin_panel/hotel_list.html', {'hotels': hotels})

def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        formset = RoomClassTemplateFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            hotel = form.save()
            formset.instance = hotel
            formset.save()
            return redirect('admin_panel:admin_hotel_list')
    else:
        form = HotelForm()
        formset = RoomClassTemplateFormSet()
    return render(request, 'admin_panel/hotel_form.html', {'form': form, 'formset': formset, 'title': 'Добавить отель'})

def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        formset = RoomClassTemplateFormSet(request.POST, request.FILES, instance=hotel)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('admin_panel:admin_hotel_list')
    else:
        form = HotelForm(instance=hotel)
        formset = RoomClassTemplateFormSet(instance=hotel)
    return render(request, 'admin_panel/hotel_form.html', {'form': form, 'formset': formset, 'title': 'Редактировать отель'})

def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    hotel.delete()
    return redirect('admin_panel:admin_hotel_list')

# === ROOM LIST ===
def room_list(request):
    rooms = Room.objects.select_related('hotel').all()
    return render(request, 'admin_panel/room_list.html', {'rooms': rooms})

# === EXCURSION CRUD ===

def excursion_list(request):
    excursions = Excursion.objects.all()
    return render(request, 'admin_panel/excursion_list.html', {'excursions': excursions})


def excursion_create(request):
    if request.method == 'POST':
        form = ExcursionForm(request.POST, request.FILES)
        availability_formset = ExcursionAvailabilityFormSet(request.POST)
        if form.is_valid() and availability_formset.is_valid():
            excursion = form.save()
            sd = form.cleaned_data.get('start_date')  # начальная дата
            ed = form.cleaned_data.get('end_date')    # конечная дата
            if sd and ed:
                # Генерация с 10:00 по умолчанию, если не указано
                generate_excursion_schedule(excursion, sd, ed, '10:00')
            availability_formset.instance = excursion
            availability_formset.save()
            return redirect('admin_panel:excursion_list')
    else:
        form = ExcursionForm()
        availability_formset = ExcursionAvailabilityFormSet()
    return render(request, 'admin_panel/excursion_form.html', {
        'form': form,
        'availability_formset': availability_formset,
        'title': 'Добавить экскурсию'
    })


def excursion_edit(request, pk):
    excursion = get_object_or_404(Excursion, pk=pk)
    if request.method == 'POST':
        form = ExcursionForm(request.POST, request.FILES, instance=excursion)
        availability_formset = ExcursionAvailabilityFormSet(request.POST, instance=excursion)
        if form.is_valid() and availability_formset.is_valid():
            excursion = form.save()
            sd = form.cleaned_data.get('start_date')
            ed = form.cleaned_data.get('end_date')
            if sd and ed:
                # Удаляем старое расписание и генерируем новое с 10:00
                excursion.availability.all().delete()
                generate_excursion_schedule(excursion, sd, ed, '10:00')
            availability_formset.save()
            return redirect('admin_panel:excursion_list')
    else:
        form = ExcursionForm(instance=excursion)
        availability_formset = ExcursionAvailabilityFormSet(instance=excursion)
    return render(request, 'admin_panel/excursion_form.html', {
        'form': form,
        'availability_formset': availability_formset,
        'title': 'Редактировать экскурсию'
    })


def excursion_delete(request, pk):
    excursion = get_object_or_404(Excursion, pk=pk)
    if request.method == 'POST':
        excursion.delete()
        return redirect('admin_panel:excursion_list')
    return render(request, 'admin_panel/excursion_confirm_delete.html', {'excursion': excursion})

# === FLIGHT CRUD ===
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'admin_panel/flight_list.html', {'flights': flights})

def flight_create(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:flight_list')
    else:
        form = FlightForm()
    return render(request, 'admin_panel/flight_form.html', {'form': form, 'title': 'Добавить рейс'})

def flight_edit(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:flight_list')
    else:
        form = FlightForm(instance=flight)
    return render(request, 'admin_panel/flight_form.html', {'form': form, 'title': 'Редактировать рейс'})

def flight_delete(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    flight.delete()
    return redirect('admin_panel:flight_list')

# Legacy-алиасы для старых маршрутов в urls.py
flight_admin_list   = flight_list
flight_admin_create = flight_create
flight_admin_update = flight_edit
flight_admin_delete = flight_delete

# === TRAIN CRUD ===

def train_list(request):
    trains = Train.objects.all().select_related('departure_city', 'arrival_city')
    return render(request, 'admin_panel/train_list.html', {'trains': trains})


def train_edit(request, pk):
    train = get_object_or_404(Train, pk=pk)
    if request.method == 'POST':
        form = TrainForm(request.POST, instance=train)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:train_list')
    else:
        form = TrainForm(instance=train)
    return render(request, 'admin_panel/train_form.html', {'form': form, 'title': 'Редактировать поезд'})


def train_delete(request, pk):
    train = get_object_or_404(Train, pk=pk)
    train.delete()
    return redirect('admin_panel:train_list')

def train_create(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            train = form.save()
            create_tickets_for_train(train)  # ← генерируем билеты
            return redirect('admin_panel:train_list')
    else:
        form = TrainForm()
    return render(request, 'admin_panel/train_form.html', {'form': form, 'title': 'Добавить поезд'})