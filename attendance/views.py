from django.shortcuts import render
from django.http import HttpResponse
from .models import Personnel, Absence, Parade
import datetime
import logging
import sys

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
	logger = logging.getLogger(__name__)
	date = request.GET.get('date')
	date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	logger.info('DATE %s',date)

	time_of_day = int(request.GET.get('time_of_day'))
	logger.info('TIME OF DAY %s',time_of_day)
	
	try:
		parade = Parade.objects.filter(
			date = date, time_of_day = time_of_day
		)
		logger.info(parade)

		# Parade does not exist
		if len(parade) == 0:
			raise Exception('No parades found')

		else:
			parade = parade.values()[0]
			logger.info('PARADE OBJ %s',parade)

			parade_id = parade['id']
			total_strength = parade['total_strength']
			current_strength = parade['commander_strength'] + parade['personnel_strength']
			absentees = Absence.objects.filter(
				parade_id = parade_id
			).values()
			logger.info('ABSENCE %s', absentees)
			all_present = False
			if len(absentees) == 0:
				all_present = True
			
			else:
				total_attc = 0
				total_ma = 0
				total_leave = 0
				total_off = 0
				total_other = 0
				
				for abs in absentees:
					if abs['is_MC']:
						total_attc += 1
					elif abs['is_MA']:
						total_ma += 1
					elif abs['is_leave']:
						total_leave += 1
					elif abs['is_off']:
						total_off += 1
					elif abs['is_other']:
						total_other += 1
					else:
						pass

		context = {
			'parade_id': parade_id,
			'all_present': all_present,
			'total_strength': total_strength,
			'current_strength': current_strength,
			'total_absent': total_strength-current_strength,
			'total_attc': total_attc,
			'total_ma': total_ma,
			'total_leave': total_leave,
			'total_off': total_off,
			'total_other': total_other,
		}

		logger.info('RESULTS %s', context)
		return render(request, 'attendance/revhome.html/', context)
	
	except Exception as identifier:
		logging.info('ERROR %s', identifier.args[0])
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
