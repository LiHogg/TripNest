from django.views.generic import ListView, DetailView, TemplateView
from .models import Flight, FlightTicket, TrainTicket, CarReservation, MotoReservation
from location.models import Country, City
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone

# Главная страница транспорта (меню выбора транспорта)
class TransportMainView(TemplateView):
    template_name = 'transport/transport_list.html'

# --- Авиарейсы ---

def flight_list(request):
    flights = Flight.objects.all().order_by('departure_date')
    countries = Country.objects.all()
    airlines = Flight.objects.values_list('airline', flat=True).distinct().order_by('airline')

    # Получение фильтров из GET-запроса
    departure_country_id = request.GET.get('departure_country')
    departure_city_id = request.GET.get('departure_city')
    arrival_country_id = request.GET.get('arrival_country')
    arrival_city_id = request.GET.get('arrival_city')
    airline = request.GET.get('airline')
    departure_date = request.GET.get('departure_date')

    # Для выпадающих списков городов
    departure_cities = City.objects.filter(country_id=departure_country_id, has_airport=True) if departure_country_id else City.objects.none()
    arrival_cities = City.objects.filter(country_id=arrival_country_id, has_airport=True) if arrival_country_id else City.objects.none()

    # Применение фильтров к выборке рейсов
    if departure_country_id:
        flights = flights.filter(departure_city__country__id=departure_country_id)
    if departure_city_id:
        flights = flights.filter(departure_city__id=departure_city_id)
    if arrival_country_id:
        flights = flights.filter(arrival_city__country__id=arrival_country_id)
    if arrival_city_id:
        flights = flights.filter(arrival_city__id=arrival_city_id)
    if airline:
        flights = flights.filter(airline=airline)
    if departure_date:
        flights = flights.filter(departure_date__date=departure_date)

    return render(request, "transport/flightticket_list.html", {
        "flights": flights,
        "countries": countries,
        "airlines": airlines,
        "departure_cities": departure_cities,
        "arrival_cities": arrival_cities,
    })

# Ajax-запрос для получения городов по стране
def cities_by_country(request):
    country_id = request.GET.get('country_id')
    # Показывать только города с аэропортом
    cities = City.objects.filter(country_id=country_id, has_airport=True).order_by('name')
    data = [{'id': city.id, 'name': city.name} for city in cities]
    return JsonResponse({'cities': data})

# Детальная страница по рейсу
class FlightDetailView(DetailView):
    model = Flight
    template_name = 'transport/flight_detail.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.object.tickets.filter(
            is_booked=False
        ).filter(
            Q(reserved_until__isnull=True) | Q(reserved_until__lte=timezone.now())
        )
        return context
# --- ЖД билеты ---

class TrainTicketListView(ListView):
    model = TrainTicket
    template_name = 'transport/trainticket_list.html'
    context_object_name = 'trains'
    paginate_by = 20

class TrainTicketDetailView(DetailView):
    model = TrainTicket
    template_name = 'transport/trainticket_detail.html'
    context_object_name = 'train'

# --- Авто и мото ---

class CarReservationListView(ListView):
    model = CarReservation
    template_name = 'transport/carreservation_list.html'
    context_object_name = 'cars'
    paginate_by = 20

class CarReservationDetailView(DetailView):
    model = CarReservation
    template_name = 'transport/carreservation_detail.html'
    context_object_name = 'car'

class MotoReservationListView(ListView):
    model = MotoReservation
    template_name = 'transport/motoreservation_list.html'
    context_object_name = 'motos'
    paginate_by = 20

class MotoReservationDetailView(DetailView):
    model = MotoReservation
    template_name = 'transport/motoreservation_detail.html'
    context_object_name = 'moto'

# --- Автоматическая генерация билетов под рейс ---
def create_tickets_for_flight(flight, prices=None):
    prices = prices or {
        'economy': 5000,
        'standard': 8000,
        'business': 16000,
        'first': 30000,
    }
    for flight_class, seats in [
        ('economy', flight.seats_economy),
        ('standard', flight.seats_standard),
        ('business', flight.seats_business),
        ('first', flight.seats_first),
    ]:
        for seat in range(1, seats + 1):
            FlightTicket.objects.create(
                flight=flight,
                seat_number=seat,
                flight_class=flight_class,
                price=prices.get(flight_class, 0)
            )
