from django.urls import path
from .views import (
    TransportMainView,
    flight_list,
    FlightDetailView,
    TrainListView,
    TrainDetailView,
    CarReservationListView,
    CarReservationDetailView,
    MotoReservationListView,
    MotoReservationDetailView,
    cities_by_country,
)

app_name = 'transport'

urlpatterns = [
    # Главное меню транспорта
    path('', TransportMainView.as_view(), name='transport_list'),

    # Авиарейсы
    path('flights/', flight_list, name='flight_list'),
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),

    # Ж/Д-поезда
    path('trains/', TrainListView.as_view(), name='train_list'),
    path('trains/<int:pk>/', TrainDetailView.as_view(), name='train_detail'),

    # Авто
    path('cars/', CarReservationListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarReservationDetailView.as_view(), name='car_detail'),

    # Мото
    path('motos/', MotoReservationListView.as_view(), name='moto_list'),
    path('motos/<int:pk>/', MotoReservationDetailView.as_view(), name='moto_detail'),

    # AJAX: динамическая подгрузка городов по стране
    path('ajax/cities/', cities_by_country, name='ajax_cities_by_country'),
]
