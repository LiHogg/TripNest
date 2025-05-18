from django.views.generic import ListView, DetailView
from .models import FlightTicket, TrainTicket, CarReservation, MotoReservation
from django.views.generic import TemplateView


class TransportMainView(TemplateView):
    template_name = 'transport/transport_list.html'


# FlightTicket Views
class FlightTicketListView(ListView):
    model = FlightTicket
    template_name = 'transport/flightticket.html'
    context_object_name = 'flights'
    paginate_by = 20


class FlightTicketDetailView(DetailView):
    model = FlightTicket
    template_name = 'transport/flightticket_detail.html'
    context_object_name = 'flight'


# TrainTicket Views
class TrainTicketListView(ListView):
    model = TrainTicket
    template_name = 'transport/trainticket_list.html'
    context_object_name = 'trains'
    paginate_by = 20


class TrainTicketDetailView(DetailView):
    model = TrainTicket
    template_name = 'transport/trainticket_detail.html'
    context_object_name = 'train'


# CarReservation Views
class CarReservationListView(ListView):
    model = CarReservation
    template_name = 'transport/carreservation_list.html'
    context_object_name = 'cars'
    paginate_by = 20


class CarReservationDetailView(DetailView):
    model = CarReservation
    template_name = 'transport/carreservation_detail.html'
    context_object_name = 'car'


# MotoReservation Views
class MotoReservationListView(ListView):
    model = MotoReservation
    template_name = 'transport/motoreservation_list.html'
    context_object_name = 'motos'
    paginate_by = 20


class MotoReservationDetailView(DetailView):
    model = MotoReservation
    template_name = 'transport/motoreservation_detail.html'
    context_object_name = 'moto'

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
                price=prices[flight_class]
            )
