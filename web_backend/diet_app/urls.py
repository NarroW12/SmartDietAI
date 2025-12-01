from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/calendar-events/', views.calendar_api, name='calendar_api'),
]