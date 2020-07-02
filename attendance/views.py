from django.shortcuts import render
from django.http import HttpResponse
from .models import Personnel, Absence, Parade

def home_view(request):
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

def parade_view(request):

	date = request.GET.get('date')
	time_of_day = request.GET.get('time_of_day')
	
	try:
		parade = Parade.objects.filter(
			date = date, time_of_day = time_of_day
		)

		# Parade does not exist
		if len(parade) == 0:
			raise Exception('No parades found')

		else:
			parade = parade.values()[0]
			parade_id = parade['id']
			absentees = Absence.objects.filter(
				parade_id = parade_id
			)

			if len(absence) == 0:
				raise Exception('No absentees recorded')

			else:
				context = {
					'parade': parade,
					'absentees': absentees
				}
				return render(request, 'attendance/revhome.html/', context)
	
	except Exception as identifier:
		context = {
			'error': True,
			'message': identifier.args[0]
		}
		return render(request, 'attendance/revhome.html/', context)



def dashboard_view(request):
	return render(request, 'attendance/revdashboard.html/')

def troll_view(request):
	return render(request, 'attendance/jokie.html/')

def faq_view(request):
	return render(request, 'attendance/FAQ.html/')
