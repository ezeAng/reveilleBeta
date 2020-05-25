from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home, name ='attendance-home'),
    path('dashboard/', views.dashboard, name ='attendance-dashboard'),
]
