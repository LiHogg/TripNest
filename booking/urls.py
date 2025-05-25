from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),  # просмотр корзины
    path('cart/add/<int:ticket_id>/', views.add_to_cart, name='add_to_cart'),  # добавление билета
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # удаление билета
    path('cart/confirm/', views.confirm_booking, name='confirm_booking'),  # оформление бронирования
    path('my-bookings/', views.my_bookings, name='my_bookings'),  # список бронирований пользователя
    path('cart/add-hotel/', views.add_room_to_cart, name='add_room_to_cart'),
    path('cart/add-excursion/', views.add_excursion_to_cart, name='add_excursion_to_cart'),

    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),

]
