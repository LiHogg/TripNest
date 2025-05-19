from datetime import timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from location.models import Country, City
from .models import Hotel, Room, RoomInventory

# Утилита для перебора диапазона дат
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Подсчёт доступных номеров по каждому классу
def get_available_rooms_by_class(hotel, check_in, check_out):
    availability = {}
    for room_class, _ in Room.ROOM_CLASSES:
        rooms = Room.objects.filter(hotel=hotel, room_class=room_class)
        available_count = 0

        for room in rooms:
            inventory = RoomInventory.objects.filter(
                room=room,
                date__gte=check_in,
                date__lt=check_out,
                is_booked=True
            )
            if not inventory.exists():
                available_count += 1

        availability[room_class] = available_count
    return availability

# Список всех отелей с фильтрами
def hotel_list(request):
    countries = Country.objects.prefetch_related('cities').all()
    hotels = Hotel.objects.all()

    # Фильтрация
    city_id = request.GET.get('city')
    hotel_type = request.GET.get('type')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    with_kids = request.GET.get('kids') == 'on'

    if city_id:
        hotels = hotels.filter(city_id=city_id)
    if hotel_type:
        hotels = hotels.filter(type=hotel_type)
    if price_min:
        hotels = hotels.filter(price__gte=price_min)
    if price_max:
        hotels = hotels.filter(price__lte=price_max)
    if with_kids:
        hotels = hotels.filter(for_kids=True)

    return render(request, 'hotel/hotel_list.html', {
        'countries': countries,
        'hotels': hotels
    })

# AJAX-запрос: получить города по стране
def get_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)

# Детали отеля и свободные номера по классам
def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    # Получаем даты из GET или ставим сегодня/завтра
    try:
        check_in = date.fromisoformat(request.GET.get('check_in'))
        check_out = date.fromisoformat(request.GET.get('check_out'))
    except (TypeError, ValueError):
        today = date.today()
        check_in = today
        check_out = today + timedelta(days=1)

    availability = get_available_rooms_by_class(hotel, check_in, check_out)

    return render(request, 'hotel/hotel_detail.html', {
        'hotel': hotel,
        'availability': availability,
        'check_in': check_in,
        'check_out': check_out,
    })

# Страница одного номера
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'hotel/room_detail.html', {
        'room': room,
    })
