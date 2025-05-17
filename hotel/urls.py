from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('room/<int:pk>/', views.room_detail, name='room_detail'),

]
