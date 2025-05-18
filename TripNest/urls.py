from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # 1) Админка Django
    path('admin/', admin.site.urls),

    path('', include(('trip.urls', 'trip'), namespace='trip')),
    path(
        'user/',
        include(('user_profile.urls', 'user_profile'), namespace='user_profile')
    ),
    # 2) Кастомный логин/логаут/регистрация
    path('user/login/',  auth_views.LoginView.as_view(
        template_name='user_profile/login.html'
    ), name='login'),
    path('user/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('user/register/', include(('user_profile.urls','user_profile'), namespace='user_profile')),
    path('accounts/login/', lambda req: redirect('login', permanent=False)),

    # 3) Прочие приложения
    path('hotels/',     include(('hotel.urls','hotel'),       namespace='hotel')),
    path('excursions/', include(('excursion.urls','excursion'), namespace='excursion')),
    path('calendar/',   include(('calendar_app.urls','calendar_app'), namespace='calendar_app')),
    path('admin_panel/',include(('admin_panel.urls','admin_panel'), namespace='admin_panel')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
