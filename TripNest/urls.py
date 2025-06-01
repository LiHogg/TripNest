from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1) Админка Django
    path('admin/', admin.site.urls),

    # Главная страница и маршрут trip
    path('', include(('trip.urls', 'trip'), namespace='trip')),

    # Пользователи и аутентификация (использует user_profile.urls)
    path('user/', include(('user_profile.urls', 'user_profile'), namespace='user_profile')),

    # Прочие приложения
    path('hotels/', include(('hotel.urls', 'hotel'), namespace='hotel')),
    path('excursions/', include(('excursion.urls', 'excursion'), namespace='excursion')),
    path('calendar/', include(('calendar_app.urls', 'calendar_app'), namespace='calendar_app')),
    path('admin_panel/', include(('admin_panel.urls', 'admin_panel'), namespace='admin_panel')),
    path('transport/', include(('transport.urls', 'transport'), namespace='transport')),
    path('booking/', include('booking.urls')),
]

# Обслуживание статики и медиа-файлов даже при DEBUG = False
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
