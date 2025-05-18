from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        # уже залогинен — отправляем на dashboard
        return redirect('trip:home_user')
    # не залогинен — показываем гостевую
    return render(request, 'trip/home_guest.html')


@login_required
def home_user(request):
    return render(request, 'trip/home_user.html')

def coming_soon(request):
    return render(request, 'trip/coming_soon.html')