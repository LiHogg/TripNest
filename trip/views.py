from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home_guest(request):
    """Главная страница для гостей"""
    return render(request, 'trip/home_guest.html')

@login_required
def home_user(request):
    """Главная страница для авторизованных пользователей"""
    return render(request, 'trip/home_user.html')
