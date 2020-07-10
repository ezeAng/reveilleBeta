from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Personnel, Absence, Parade
import datetime
import logging
import sys
from django.db import transaction
from reveille.utils import ParadeStateHandler

def home_view(request):
	context = {'default': True}
	return render(request, 'attendance/revhome.html/', context)

def parade_view(request):
	logger = logging.getLogger(__name__)
	date = request.GET.get('date')
	formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	logger.info('DATE %s',formatted_date)

	time_of_day = int(request.GET.get('time_of_day'))
	logger.info('TIME OF DAY %s',time_of_day)
	transaction.set_autocommit(False)

	
	# try:
	parade = Parade.objects.filter(
		date = formatted_date, time_of_day = time_of_day
	)
	logger.info('PARADE %s', parade)
	parade_summary = None
	parade_overview = None

	if len(parade) == 0:
		logger.info('Lanjiao')
		parade_exist = False

	else:
		logger.info('jibai')
		parade_exist = True
		parade = parade.values()[0]
		logger.info('PARADE OBJ %s',parade)

		parade_id = parade['id']

		parade_instance = ParadeStateHandler(parade_id)			
		parade_absence_summary = parade_instance.calc_absence()
		
		parade_summary = {
			'parade_id': parade_id,
			'total_strength': parade['total_strength'],
			'current_strength': parade['current_strength'],
			'commander_strength': parade['commander_strength'],
			'personnel_strength': parade['personnel_strength']
		}
		parade_summary.update(parade_absence_summary)
		parade_overview = parade_instance.get_parade_overview()

	
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

			parade_instance = ParadeStateHandler(parade_id)
			parade_instance.update_parade_instance()
		
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
			'parade_overview': parade_overview
		}

		logger.info('RESULTS %s', context)
		return render(request, 'attendance/revhome.html/', context)
	
	else:
		raise Exception('Method not allowed')
	
	# except Exception as identifier:
	# 	logging.info('ERROR %s', identifier.args[0])
	# 	context = {
	# 		'error': True,
	# 		'message': 'Hong gan liao unexpected error occured. Please contact your encik for support.'
	# 	}
	# 	return render(request, 'attendance/revhome.html/', context)

def dashboard_view(request):
	return render(request, 'attendance/revdashboard.html/')

def troll_view(request):
	return render(request, 'attendance/jokie.html/')

def faq_view(request):
	return render(request, 'attendance/FAQ.html/')


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