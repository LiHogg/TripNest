from django.urls import path
from . import views

app_name = 'trip'

urlpatterns = [
    path('', views.home_user,   name='home_user'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    # остальные пути…
]
