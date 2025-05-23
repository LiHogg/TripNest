from django.urls import path
from . import views
app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # === USER CRUD ===
    path('admin_panel:users/', views.user_list, name='user_list'),
    path('users/edit/<int:id>/', views.user_edit, name='user_edit'),
    path('users/deactivate/<int:id>/', views.user_deactivate, name='user_deactivate'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),

    # === COUNTRY CRUD ===
    path('location/country/', views.country_list, name='admin_country_list'),
    path('location/country/create/', views.country_create, name='admin_country_create'),
    path('location/country/edit/<int:pk>/', views.country_edit, name='admin_country_edit'),
    path('location/country/delete/<int:pk>/', views.country_delete, name='admin_country_delete'),

    # === CITY CRUD ===
    path('location/city/', views.city_list, name='admin_city_list'),
    path('location/city/create/', views.city_create, name='admin_city_create'),
    path('location/city/edit/<int:pk>/', views.city_edit, name='admin_city_edit'),
    path('location/city/delete/<int:pk>/', views.city_delete, name='admin_city_delete'),

    # === HOTEL + ROOM CRUD ===
    path('location/hotel/', views.hotel_list, name='admin_hotel_list'),
    path('location/hotel/create/', views.hotel_create, name='admin_hotel_create'),
    path('location/hotel/edit/<int:pk>/', views.hotel_edit, name='admin_hotel_edit'),
    path('location/hotel/delete/<int:pk>/', views.hotel_delete, name='admin_hotel_delete'),
    path('rooms/', views.room_list, name='admin_room_list'),

    # === EXCURSION CRUD ===
    path('excursion/', views.excursion_list,   name='excursion_list'),
    path('excursion/create/', views.excursion_create, name='admin_excursion_create'),
    path('excursion/edit/<int:pk>/',   views.excursion_edit,   name='admin_excursion_edit'),
    path('excursion/delete/<int:pk>/', views.excursion_delete, name='admin_excursion_delete'),

    # === FLIGHT CRUD ===
    path('flights/', views.flight_admin_list, name='flight_list'),
    path('flights/create/', views.flight_admin_create, name='flight_create'),
    path('flights/<int:pk>/edit/', views.flight_admin_update, name='flight_update'),
    path('flights/<int:pk>/delete/', views.flight_admin_delete, name='flight_delete'),

    # === TRAIN CRUD ===

    path('trains/', views.train_list, name='train_list'),
    path('trains/create/', views.train_create, name='train_create'),
    path('trains/<int:pk>/edit/', views.train_edit, name='train_edit'),
    path('trains/<int:pk>/delete/', views.train_delete, name='train_delete'),

]