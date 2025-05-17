from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from location.models import Country, City
from .models import Hotel,Room


def hotel_list(request):
    countries = Country.objects.prefetch_related('cities').all()
    hotels = Hotel.objects.all()

    # Фильтрация
    city_id   = request.GET.get('city')
    hotel_type= request.GET.get('type')
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

def get_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    # передаём в шаблон список доступных комнат
    rooms = hotel.rooms.filter(available=True)
    return render(request, 'hotel/hotel_detail.html', {
        'hotel': hotel,
        'rooms': rooms,
    })

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'hotel/room_detail.html', {
        'room': room,
    })



def get_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)



def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    # Раньше было .filter(available=True) — убираем, берём все комнаты
    rooms = hotel.rooms.all()
    return render(request, 'hotel/hotel_detail.html', {
        'hotel': hotel,
        'rooms': rooms,
    })