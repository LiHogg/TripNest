from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Стандартная админ-панель Django
    path('admin/', admin.site.urls),

    # Основной роутинг приложения trip
    path('', include(('trip.urls', 'trip'), namespace='trip')),

    # Кастомная админ-панель для управления контентом
    path('admin_panel/', include(('admin_panel.urls', 'admin_panel'), namespace='admin_panel')),

    # Профиль пользователя
    path('user/', include(('user_profile.urls', 'user_profile'), namespace='user_profile')),

    # Аутентификация
    path('accounts/login/',  auth_views.LoginView.as_view(),  name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Прочие приложения
    path('hotels/',    include(('hotel.urls', 'hotel'), namespace='hotel')),
    path('calendar/',  include(('calendar_app.urls', 'calendar_app'), namespace='calendar_app')),
    path('excursion/', include(('excursion.urls', 'excursion'), namespace='excursion')),
]

# Статические и медиа-файлы в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
