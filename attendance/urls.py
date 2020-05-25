from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name ='attendance-home'),
    path('admin/', views.admin, name ='attendance-admin'),
]
