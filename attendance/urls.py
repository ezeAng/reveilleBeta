from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name ='attendance-home'),
    path('parade/', views.parade_view, name = 'attendance-parade'),
    # path('dashboard/', views.dashboard_view, name ='attendance-dashboard'),
    path('troll/',views.troll_view, name='attendance-troll'),
    path('faq/',views.faq_view, name='attendance-faq'),
]
