from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home_view, name ='attendance-home'),
    path('dashboard/', views.dashboard_view, name ='attendance-dashboard'),
    path('troll/',views.troll_view, name='attendance-troll'),
]
