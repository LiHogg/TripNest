from django.shortcuts import render, get_object_or_404, redirect
from .models import Excursion
from .forms import ExcursionForm, ExcursionAvailabilityFormSet

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
    return render(request, 'excursion/excursion_detail.html', {
        'excursion': excursion,
        'availability': availability
    })

