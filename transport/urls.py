from django.urls import path
from . import views
from .views import TransportMainView

app_name = 'transport'

urlpatterns = [
    path('', TransportMainView.as_view(), name='transport_main'),  # маршрут по умолчанию

    # Flight tickets
    path('flights/', views.FlightTicketListView.as_view(), name='flight_list'),
    path('flights/<int:pk>/', views.FlightTicketDetailView.as_view(), name='flight_detail'),

    # Train tickets
    path('trains/', views.TrainTicketListView.as_view(), name='train_list'),
    path('trains/<int:pk>/', views.TrainTicketDetailView.as_view(), name='train_detail'),

    # Car reservations
    path('cars/', views.CarReservationListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarReservationDetailView.as_view(), name='car_detail'),

    # Motorcycle reservations
    path('motos/', views.MotoReservationListView.as_view(), name='moto_list'),
    path('motos/<int:pk>/', views.MotoReservationDetailView.as_view(), name='moto_detail'),
]
