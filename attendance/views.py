from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Personnel, Absence, Parade
import datetime
import logging
import sys
from django.db import transaction
from .utils import ParadeStateHandler, CardHandler

def home_view(request):
	context = {'default': True}
	return render(request, 'attendance/MainHTML/revhome.html/', context)

def parade_view(request):
	logger = logging.getLogger(__name__)
	date = request.GET.get('date')
	formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	time_of_day = int(request.GET.get('time_of_day'))
	logger.info('DATE %s',formatted_date)
	logger.info('TIME OF DAY %s',time_of_day)
	# transaction.set_autocommit(False)

	try:
		parade = Parade.objects.filter(
			date = formatted_date, time_of_day = time_of_day
		)
		logger.info('PARADE %s', parade)
		parade_summary = None
		parade_overview = None

		if len(parade) == 0:
			parade_exist = False

		else:
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
			'''
			action enums
			add: 0
			edit: 1
			delete: 2
			'''
			logger.info('POST DATA %s', request.POST)
			name = request.POST.get('Name')
			remarks = request.POST.get('Remarks')
			reason = request.POST.get('Absence')
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
				
				card_instance = CardHandler(
					parade_id = parade_id,
					name = name,
					remarks= remarks,
					reason = reason
				)
				if card_instance.add_new_card() == False:
					context = {
						'repeat_entry': True,
						'message': "This personnel's record already exists for this parade. Edit the existing card instead"
					}
					render(request, 'attendance/MainHTML/revhome.html/', context)
				else:
					pass

			except Exception as identifier:
				transaction.rollback()
				raise Exception(identifier.args[0])
			transaction.commit()

			return HttpResponseRedirect(
				request.path_info + '?date=' + date + '&time_of_day=' + str(time_of_day))
		

		elif request.method == 'GET':
			context = {
				'parade_exist': parade_exist,
				'parade_summary': parade_summary,
				'parade_overview': parade_overview
			}

			logger.info('RESULTS %s', context)
			return render(request, 'attendance/MainHTML/revhome.html/', context)
		
		else:
			raise Exception('Method not allowed')
	
	except Exception as identifier:
		logging.info('ERROR %s', identifier.args[0])
		context = {
			'error': True,
			'message': 'Hong gan liao unexpected error occured. Please contact your encik for support.'
		}
		return render(request, 'attendance/MainHTML/revhome.html/', context)

def troll_view(request):
	return render(request, 'attendance/MainHTML/jokie.html/')

def faq_view(request):
	return render(request, 'attendance/MainHTML/FAQ.html/')



'''
CBV [KIV]
'''
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