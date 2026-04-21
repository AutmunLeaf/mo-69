"""
Конфигурация URL для проекта mo69_diplom.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),
    
    # Приложение acts (акты КС-2/КС-3)
    path('', include('acts.urls')),
    
    # Аутентификация через Django auth
    path('login/', auth_views.LoginView.as_view(template_name='acts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Редирект с /accounts/profile/ на dashboard
    path('accounts/profile/', RedirectView.as_view(url='/dashboard/', permanent=False)),
]
