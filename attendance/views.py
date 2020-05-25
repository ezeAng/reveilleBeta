from django.shortcuts import render
from django.http import HttpResponse
from attendance.models import Trooper, Absence

def home_view(request):

	context = {
		"trooper_name": Trooper.objects.all() ,
        "trooper_platoon": Trooper.objects.all() #retrive from db

	}
	return render(request, 'attendance/revhome.html/', context)

def dashboard_view(request):
	return render(request, 'attendance/revdashboard.html/')
