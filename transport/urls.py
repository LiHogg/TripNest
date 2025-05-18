from django.urls import path
from . import views
from .views import (
    TransportMainView,
    flight_list,          # функция для списка авиарейсов с фильтрацией
    FlightDetailView,
    TrainTicketListView, TrainTicketDetailView,
    CarReservationListView, CarReservationDetailView,
    MotoReservationListView, MotoReservationDetailView,
)

app_name = 'transport'

urlpatterns = [
    path('', TransportMainView.as_view(), name='transport_list'),  # <-- меняем имя

    # Авиабилеты
    path('flights/', flight_list, name='flight_list'),  # фильтрация через функцию
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),

    # ЖД-билеты
    path('trains/', TrainTicketListView.as_view(), name='train_list'),
    path('trains/<int:pk>/', TrainTicketDetailView.as_view(), name='train_detail'),

    # Авто
    path('cars/', CarReservationListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarReservationDetailView.as_view(), name='car_detail'),

    # Мото
    path('motos/', MotoReservationListView.as_view(), name='moto_list'),
    path('motos/<int:pk>/', MotoReservationDetailView.as_view(), name='moto_detail'),

    # AJAX: для динамической подгрузки городов по стране
    path('ajax/cities/', views.cities_by_country, name='ajax_cities_by_country'),
]
