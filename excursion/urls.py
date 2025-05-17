from django.urls import path
from . import views

app_name = 'excursion'

urlpatterns = [
    path('', views.excursion_list,   name='excursion_list'),
    path('<int:pk>/', views.excursion_detail, name='excursion_detail'),
  ]
