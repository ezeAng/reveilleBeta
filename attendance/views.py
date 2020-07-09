from django.shortcuts import render
from django.http import HttpResponse
from .models import Personnel, Absence, Parade
import datetime
import logging
import sys

def home_view(request):
	# parade_id = request.GET.get('parade_id')
	# if parade_id is None:
	# 	context = {
	# 		'error': True
	# 	}
	# 	return render(request, 'attendance/revhome.html/', context)
	# else:
	# 	context = {
	# 		'error': False,
	# 		'parade': Parade.objects.filter(id=parade_id).values()[0],
	# 	}
	context = {'default': True}
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
			parade_exist = False

		else:
			parade_exist = True
			parade = parade.values()[0]
			logger.info('PARADE OBJ %s',parade)

			parade_id = parade['id']
			total_strength = parade['total_strength']
			current_strength = parade['commander_strength'] + parade['personnel_strength']
			
			absentees = Absence.objects.filter(
				parade_id = parade_id
			).values()
			logger.info('ABSENCE %s', absentees)
			
			no_absentees = True
			if len(absentees) == 0:
				no_absentees = False
				card_data = []
			
			else:
				total_attc = 0
				total_ma = 0
				total_leave = 0
				total_off = 0
				total_other = 0
				
				card_data = []
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
					
					personnel = Personnel.objects.get(
						id=int(abs['personnel_id']))
					data = {
						'name': personnel.name,
						'rank': personnel.rank,
						'platoon': personnel.platoon,
						'is_mc': abs['is_MC'],
						'is_ma': abs['is_MA'],
						'is_leave': abs['is_leave'],
						'is_off': abs['is_off'],
						'is_other': abs['is_other'],
						'remarks': abs['remarks'],
					}
					logger.info('DATA %s', data )
					card_data.append(data)
					logger.info('CARD DATA %s', card_data )

		parade_summary = {
			'parade_id': parade_id,
			'no_absentees': no_absentees,
			'total_strength': total_strength,
			'current_strength': current_strength,
			'total_absent': total_strength-current_strength,
			'total_attc': total_attc,
			'total_ma': total_ma,
			'total_leave': total_leave,
			'total_off': total_off,
			'total_other': total_other,
		}

		if request.method == 'GET':
			context = {
				'parade_exist': parade_exist,
				'parade_summary': parade_summary,
				'parade_overview': card_data
			}

			logger.info('RESULTS %s', context)
			return render(request, 'attendance/revhome.html/', context)
		
		if request.method == 'POST':
			logger.info('POST DATA %s', request.POST)
			if parade_exist:
					
			
			else:
				# create new parade if it does not exist
				parade = Parade(

				)
				parade.save()
				return parade
			# '''
			absence = Absence(
				personnel = personnel_object,
				parade = 

			)
			# '''
	
	except Exception as identifier:
		logging.info('ERROR %s', identifier.args[0])
		context = {
			'error': True,
			'message': 'Hong gan liao unexpected error occured. Please contact your encik grandmother for support.'
		}
		return render(request, 'attendance/revhome.html/', context)

# def add_card_view(request):
	

def dashboard_view(request):
	return render(request, 'attendance/revdashboard.html/')

def troll_view(request):
	return render(request, 'attendance/jokie.html/')

def faq_view(request):
	return render(request, 'attendance/FAQ.html/')
