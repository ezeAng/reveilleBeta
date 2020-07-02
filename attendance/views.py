from django.shortcuts import render
from django.http import HttpResponse
from .models import Personnel, Absence, Parade

def home_view(request):
	'''
		locoalhost:8000/home/?parade_id=1
	'''
	parade_id = request.GET.get('parade_id')
	if parade_id is None:
		context = {
			'error': True
		}
		return render(request, 'attendance/revhome.html/', context)
	else:
		# parade = Parade.objects.get(id=parade_id)
		context = {
			'error': False,
			# 'personnel': Personnel.objects.all(),
			'parade': Parade.objects.filter(id=parade_id).values()[0],
			# 'parade': parade


			

		}
		return render(request, 'attendance/revhome.html/', context)

def dashboard_view(request):
	return render(request, 'attendance/revdashboard.html/')

def troll_view(request):
	return render(request, 'attendance/jokie.html/')

def faq_view(request):
	return render(request, 'attendance/FAQ.html/')
