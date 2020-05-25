from django.shortcuts import render
from django.http import HttpResponse
from .models import Personnel, Absence

def home(request):
    
	context = {
		'posts': Personnel.objects.all()
	}
	return render(request, 'attendance/revhome.html/', context)

def dashboard(request):
	return render(request, 'attendance/revdashboard.html/')
