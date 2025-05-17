from django.urls import path, include
from trip.views import home_guest, home_user  # <-- Исправлен импорт
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home_guest, name='home_guest'),
    path('home/', home_user, name='home_user'),
    path('admin/', include('admin_panel.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('user/', include('user_profile.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home_guest'), name='logout'),  # <-- Добавлено
    path('hotels/', include('hotel.urls')),
    path('calendar/', include('calendar_app.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
