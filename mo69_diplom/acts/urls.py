"""
URL-маршруты для приложения актов КС-2/КС-3.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Главная страница - дашборд
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Акты
    path('acts/create/', views.create_act, name='create_act'),
    path('acts/<int:pk>/', views.act_detail, name='act_detail'),
    path('acts/<int:pk>/ks2/pdf/', views.generate_ks2_pdf, name='generate_ks2_pdf'),
    path('acts/<int:pk>/ks3/pdf/', views.generate_ks3_pdf, name='generate_ks3_pdf'),
    path('acts/<int:pk>/ks2/xml/', views.generate_ks2_xml_file, name='generate_ks2_xml'),
    path('acts/<int:pk>/ks3/xml/', views.generate_ks3_xml_file, name='generate_ks3_xml'),
    
    # Валидация XML
    path('validate-xml/', views.validate_xml_page, name='validate_xml'),
    
    # Справочники
    path('contractors/', views.contractors_list, name='contractors_list'),
    path('objects/', views.objects_list, name='objects_list'),
    path('contracts/', views.contracts_list, name='contracts_list'),
    path('work-types/', views.work_types_list, name='work_types_list'),
]
