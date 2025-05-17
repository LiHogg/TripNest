from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from user_profile.models import Profile, Passport, DriverLicense, LoginHistory, History
from location.models import Country, City
from hotel.models import Hotel, Room
from .forms import CountryForm, CityForm, HotelForm
from hotel.forms import RoomForm

# === DASHBOARD ===
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

# === USER LIST ===
def user_list(request):
    users = User.objects.all().select_related(
        'profile',
        'passport',
        'driver_license',
    )
    return render(request, 'admin_panel/user_list.html', {'users': users})

# === USER EDIT ===
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
        return redirect('user_list')

    context = {
        'user': user,
        'profile': profile,
        'passport': passport,
        'license': license,
        'history': history,
    }
    return render(request, 'admin_panel/user_edit.html', context)

# === USER DEACTIVATE ===
def user_deactivate(request, id):
    user = get_object_or_404(User, id=id)
    user.is_active = False
    user.save()
    return redirect('user_list')

# === USER DELETE ===
def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('user_list')

# === COUNTRY LIST ===
def country_list(request):
    countries = Country.objects.all()
    return render(request, 'admin_panel/country_list.html', {'countries': countries})


def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_country_list')
    else:
        form = CountryForm()
    return render(request, 'admin_panel/country_form.html', {'form': form, 'title': 'Добавить страну'})


def country_edit(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('admin_country_list')
    else:
        form = CountryForm(instance=country)
    return render(request, 'admin_panel/country_form.html', {'form': form, 'title': 'Редактировать страну'})


def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    return redirect('admin_country_list')

# === CITY LIST ===
def city_list(request):
    cities = City.objects.select_related('country').all()
    return render(request, 'admin_panel/city_list.html', {'cities': cities})


def city_create(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_city_list')
    else:
        form = CityForm()
    return render(request, 'admin_panel/city_form.html', {'form': form, 'title': 'Добавить город'})


def city_edit(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('admin_city_list')
    else:
        form = CityForm(instance=city)
    return render(request, 'admin_panel/city_form.html', {'form': form, 'title': 'Редактировать город'})


def city_delete(request, pk):
    city = get_object_or_404(City, pk=pk)
    city.delete()
    return redirect('admin_city_list')

# === HOTEL LIST ===
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'admin_panel/hotel_list.html', {'hotels': hotels})


def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_hotel_list')
    else:
        form = HotelForm()
    return render(request, 'admin_panel/hotel_form.html', {'form': form, 'title': 'Добавить отель'})

# === HOTEL EDIT ===
def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('admin_hotel_list')
    else:
        form = HotelForm(instance=hotel)

    return render(request, 'admin_panel/hotel_form.html', {'form': form, 'title': 'Редактировать отель'})

# === HOTEL DELETE ===
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    hotel.delete()
    return redirect('admin_hotel_list')

# === ROOM CRUD ===
def room_list(request):
    rooms = Room.objects.select_related('hotel').all()
    return render(request, 'admin_panel/room_list.html', {'rooms': rooms})


def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_room_list')
    else:
        form = RoomForm()
    return render(request, 'admin_panel/room_form.html', {'form': form, 'title': 'Добавить номер'})


def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('admin_room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'admin_panel/room_form.html', {'form': form, 'title': 'Редактировать номер'})


def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('admin_room_list')
    return render(request, 'admin_panel/room_confirm_delete.html', {'room': room})