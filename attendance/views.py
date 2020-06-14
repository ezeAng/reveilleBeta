from django.shortcuts import render
from django.http import HttpResponse
from .models import Personnel, Absence

def home_view(request):

	context = {
		'posts': Personnel.objects.all()
	}
	return render(request, 'attendance/revhome.html/', context)

def dashboard_view(request):
	return render(request, 'attendance/revdashboard.html/')

def troll_view(request):
	return render(request, 'attendance/jokie.html/')
