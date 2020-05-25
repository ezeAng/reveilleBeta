from django.shortcuts import render
from django.http import HttpResponse
from .models import Trooper, Absence

def home(request):
    
	context = {
		'posts': Trooper.objects.all()
	}
	return render(request, 'attendance/revhome.html/', context)

def dashboard(request):
	return render(request, 'attendance/revdashboard.html/')
