from django.shortcuts import render, get_object_or_404
from .models import Excursion
from .forms import ExcursionForm, ExcursionAvailabilityFormSet
from booking.models import ExcursionBooking
from django.db.models import Sum

# === LIST ===
def excursion_list(request):
    excursions = Excursion.objects.select_related('city').all()
    return render(request, 'excursion/excursion_list.html', {
        'excursions': excursions
    })

# === DETAIL ===
def excursion_detail(request, pk):
    excursion = get_object_or_404(Excursion, pk=pk)
    availability = excursion.availability.all()

    updated_availability = []
    for slot in availability:
        # Фильтруем по excursion_title (название экскурсии)
        booked = ExcursionBooking.objects.filter(
            excursion_title=excursion.name,
            date=slot.available_date
        ).aggregate(total=Sum('people'))['total'] or 0
        actual_free = slot.available_slots - booked
        updated_availability.append({
            'available_date': slot.available_date,
            'start_time': slot.start_time,
            'available_slots': max(actual_free, 0),
        })

    return render(request, 'excursion/excursion_detail.html', {
        'excursion': excursion,
        'availability': updated_availability,
    })
