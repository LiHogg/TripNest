from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from transport.models import FlightTicket
from .models import DraftBooking, BookingItem, Booking, BookingTicket, HotelBooking, ExcursionBooking
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.utils.http import urlencode


@login_required
def cart_view(request):
    # Получить все билет-ID, которые лежат в чьей-либо корзине
    reserved_in_carts = BookingItem.objects.values_list('flight_ticket_id', flat=True)

    # Удаляем просроченные резервы ТОЛЬКО у тех билетов, которых НЕТ в корзинах
    FlightTicket.objects.filter(
        reserved_until__lte=timezone.now(),
        is_booked=False
    ).exclude(id__in=reserved_in_carts).update(reserved_until=None)

    # Всё остальное как раньше
    draft, created = DraftBooking.objects.get_or_create(user=request.user)
    items = draft.items.select_related('flight_ticket__flight')

    return render(request, 'booking/cart.html', {'items': items, 'draft': draft})@login_required

def add_to_cart(request, ticket_id):
    ticket = get_object_or_404(FlightTicket, id=ticket_id, is_booked=False)

    # Пропускаем, если билет уже временно зарезервирован
    if ticket.reserved_until and ticket.reserved_until > timezone.now():
        return redirect('booking:cart')

    draft, created = DraftBooking.objects.get_or_create(user=request.user)

    if not draft.items.filter(flight_ticket=ticket).exists():
        BookingItem.objects.create(draft=draft, flight_ticket=ticket)
        ticket.reserved_until = timezone.now() + timedelta(hours=24)
        ticket.save()

    return redirect('booking:cart')

# Удалить билет из корзины
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(BookingItem, id=item_id, draft__user=request.user)
    item.delete()
    return redirect('booking:cart')

# Подтвердить заказ (оформить бронирование)
@login_required
def confirm_booking(request):
    draft = get_object_or_404(DraftBooking, user=request.user)
    items = draft.items.select_related('flight_ticket')
    if request.method == "POST":
        # Создаем подтвержденное бронирование
        booking = Booking.objects.create(user=request.user)
        for item in items:
            if item.flight_ticket and not item.flight_ticket.is_booked:
                # Помечаем билет как занятый
                item.flight_ticket.is_booked = True
                item.flight_ticket.save()
                BookingTicket.objects.create(booking=booking, flight_ticket=item.flight_ticket)
        # Очищаем корзину
        items.delete()
        return render(request, 'booking/booking_success.html', {'booking': booking})
    return render(request, 'booking/confirm_booking.html', {'items': items, 'draft': draft})

# Список всех бронирований пользователя
@login_required
def my_bookings(request):
    booking_type = request.GET.get('type')
    context = {}

    if booking_type == 'transport':
        context['title'] = "Ваши билеты на транспорт"
        context['tickets'] = FlightTicket.objects.filter(is_booked=True, booking__user=request.user)
    elif booking_type == 'hotel':
        context['title'] = "Ваши бронирования жилья"
        context['hotels'] = HotelBooking.objects.filter(user=request.user)
    elif booking_type == 'excursion':
        context['title'] = "Ваши экскурсии"
        context['excursions'] = ExcursionBooking.objects.filter(user=request.user)
    else:
        context['title'] = "Все ваши бронирования"

    return render(request, 'booking/my_bookings.html', context)


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(BookingItem, id=item_id, draft__user=request.user)
    flight_id = item.flight_ticket.flight.id

    # Очистка временного резерва
    ticket = item.flight_ticket
    ticket.reserved_until = None
    ticket.save()

    item.delete()

    return redirect('transport:flight_detail', pk=flight_id)