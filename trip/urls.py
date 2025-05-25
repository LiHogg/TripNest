from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    # 1) Главная точка входа — всегда попадает в views.home
    path('', views.home, name='home'),

    # 2) Только когда пользователь уже авторизован — свой dashboard
    path('user/', views.home_user, name='home_user'),

    # 3) Страница “скоро будет”
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    # …и другие урлы, если есть
    path('home_guest/', views.home_guest, name='home_guest'),
]
