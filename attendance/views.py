from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Personnel, Absence, Parade
import datetime
import logging
import sys
from django.db import transaction
from reveille.utils import ParadeStrengthCalculator

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

# class ParadeView(View):
# 	logger = logging.getLogger(__name__)
# 	date = request.GET.get('date')
# 	formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
# 	logger.info('DATE %s',formatted_date)

# 	time_of_day = int(request.GET.get('time_of_day'))
# 	logger.info('TIME OF DAY %s',time_of_day)

# 	def get(self, request, *args, **kwargs):
# 		pass
# 	def post(self, request, *args, **kwargs):
# 		pass

def parade_view(request):
	logger = logging.getLogger(__name__)
	date = request.GET.get('date')
	formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	logger.info('DATE %s',formatted_date)

	time_of_day = int(request.GET.get('time_of_day'))
	logger.info('TIME OF DAY %s',time_of_day)
	transaction.set_autocommit(False)

	
	try:
		parade = Parade.objects.filter(
			date = formatted_date, time_of_day = time_of_day
		)
		logger.info('PARADE %s', parade)
		card_data = []
		parade_summary = None

		# Parade does not exist
		if len(parade) == 0:
			logger.info('Lanjiao')
			parade_exist = False

		else:
			logger.info('jibai')
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
				'total_strength': total_strength,
				'current_strength': current_strength,
				
				# take from utils, do .update
				'no_absentees': no_absentees,
				'total_absent': total_strength-current_strength,
				'total_attc': total_attc,
				'total_ma': total_ma,
				'total_leave': total_leave,
				'total_off': total_off,
				'total_other': total_other,
			}

		
		if request.method == 'POST':
			logger.info('POST DATA %s', request.POST)
			name = request.POST.get('Name')
			remarks = request.POST.get('Remarks')
			absence = request.POST.get('Absence')
			transaction.set_autocommit(False)

			try:
				if parade_exist:
					pass

				else:
					parade = Parade(
						date = formatted_date, 
						time_of_day = time_of_day
					)
					parade.save()
					parade_id = parade.id
					parade_instance = ParadeStrengthCalculator(parade_id)
					parade_instance.update_parade_instance()

				personnel_obj = Personnel.objects.get(
					name = name
				)
				absence = Absence(
					personnel = personnel_obj,
					parade_id = parade_id,
					remarks = remarks,
				)
				if absence == 'MA':
					absence.is_MA = True
				elif absence == 'MC':
					absence.is_MC = True
				elif absence == 'Off':
					absence.is_off = True
				elif absence == 'Leave':
					absence.is_leave = True
				elif absence == 'Others':
					absence.is_other = True
				else:
					pass
				absence.save()
			
			except Exception as identifier:
				transaction.rollback()
				raise Exception(identifier.args[0])
			transaction.commit()

			logger.info('GET DATE %s', date)
			logger.info('GET TOD, %s', str(time_of_day))
			return HttpResponseRedirect(
				request.path_info + '?date=' + date + '&time_of_day=' + str(time_of_day))
		
		elif request.method == 'GET':
			context = {
				'parade_exist': parade_exist,
				'parade_summary': parade_summary,
				'parade_overview': card_data
			}

			logger.info('RESULTS %s', context)
			return render(request, 'attendance/revhome.html/', context)
		
		else:
			raise Exception('Method not allowed')
	
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
