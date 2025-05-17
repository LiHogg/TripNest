from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    """
    Точка входа на корень сайта.
    Если пользователь неавторизован — отрисовываем гостевую.
    Если авторизован — перенаправляем на защищённую user_home.
    """
    if not request.user.is_authenticated:
        return render(request, 'trip/home_guest.html')
    return redirect('trip:home_user')


@login_required
def home_user(request):
    """
    Главная страница для залогиненных пользователей.
    Здесь можете показать dashboard, список бронирований и т.п.
    """
    # готовим контекст, например:
    context = {
        'user': request.user,
        # 'bookings': Booking.objects.filter(user=request.user),
    }
    return render(request, 'trip/home_user.html', context)

def coming_soon(request):
    return render(request, 'trip/coming_soon.html')