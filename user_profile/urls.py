from django.urls import path
from .views import edit_profile_view, register, user_login, profile_details_view,profile_view
from django.contrib.auth import views as auth_views

app_name = 'user_profile'

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='trip:home_guest'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/details/', profile_details_view, name='profile_details'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user_profile/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='user_profile/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user_profile/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user_profile/password_reset_complete.html'),
         name='password_reset_complete'),
]
