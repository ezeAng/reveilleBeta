from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Personnel, Absence, Parade
import datetime
import logging
import sys
from django.db import transaction
from .utils import ParadeStateHandler, CardHandler
from dashboard.utils import get_all_personnel, get_search

def home_view(request):
	context = {'default': True}
	return render(request, 'attendance/MainHTML/revhome.html/', context)

def parade_view(request):
	logger = logging.getLogger(__name__)
	date = request.GET.get('date')
	formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	time_of_day = int(request.GET.get('time_of_day'))
	create = request.GET.get('create')
	logger.info('DATE %s',formatted_date)
	logger.info('TIME OF DAY %s',time_of_day)
	logger.info('CREATE %s',create)
	# transaction.set_autocommit(False)

	parade = Parade.objects.filter(
			date = formatted_date, time_of_day = time_of_day
		)
	logger.info('PARADE %s', parade)
	parade_summary = None
	parade_overview = None
	try:
		# parade does not exist
		if len(parade) == 0:
			# if user choose create
			if create is not None:
				parade = Parade(
					date = formatted_date, 
					time_of_day = time_of_day
				)
				parade_instance = ParadeStateHandler(parade_id)
				parade.save(

				)
				return HttpResponseRedirect(
					request.path_info + '?date=' + date + '&time_of_day=' + str(time_of_day))
			# if user choose select
			else:
				parade_exist=False

		# parade exists
		else:
			# route fucker who try to create existing parade back to select
			if create is not None:
				return HttpResponseRedirect(
					request.path_info + '?date=' + date + '&time_of_day=' + str(time_of_day))
			else: 
				pass

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
			action = int(request.POST.get('action'))
			logger.info('ACTION %s', action)
		
			if action == 0:
				# add card
				name = request.POST.get('searchAdd')
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
						return render(request, 'attendance/MainHTML/revhome.html/', context)
					else:
						pass

				except Exception as identifier:
					transaction.rollback()
					raise Exception(identifier.args[0])
				transaction.commit()

				return HttpResponseRedirect(
					request.path_info + '?date=' + date + '&time_of_day=' + str(time_of_day))
		
			elif action == 1:
				# edit card
				remarks = request.POST.get('Remarks')
				reason = request.POST.get('Absence')
				absence_id = int(request.POST.get('absence_id'))
				logger.info('remarks %s', remarks)
				logger.info('reason %s', reason)
				logger.info('absence_id %s', absence_id)
				transaction.set_autocommit(False)
				
				try:
					card_instance = CardHandler(
						absence_id = absence_id,
						remarks= remarks,
						reason = reason
					)
					card_instance.edit_card()

				except Exception as identifier:
					transaction.rollback()
					raise Exception(identifier.args[0])
				transaction.commit()

				return HttpResponseRedirect(
					request.path_info + '?date=' + date + '&time_of_day=' + str(time_of_day))
		
			elif action == 2:
				# delete card
				absence_id = int(request.POST.get('absence_id'))
				logger.info('absence_id %s', absence_id)
				transaction.set_autocommit(False)
				
				try:
					card_instance = CardHandler(
						absence_id = absence_id,
						parade_id = parade_id,
					)
					card_instance.delete_card()

				except Exception as identifier:
					transaction.rollback()
					raise Exception(identifier.args[0])
				transaction.commit()

				return HttpResponseRedirect(
					request.path_info + '?date=' + date + '&time_of_day=' + str(time_of_day))
		
				pass
			
			elif action == 3:
				# delete parade
				transaction.set_autocommit(False)
				try:
					if parade_exist:
						parade = Parade.objects.get(
							id = parade_id
						)
						parade.delete()
					else:
						raise Exception('Cannot delete non-existent parade.')
				except Exception as identifier:
					transaction.rollback
					raise Exception(identifier.args[0])
				transaction.commit()

			else:
				raise Exception('Invalid action type')

		elif request.method == 'GET':
			context = {
				'parade_exist': parade_exist,
				'parade_summary': parade_summary,
				'parade_overview': parade_overview,
				'personnel': get_search(),
				'absentees': get_search(parade_id)
			}

			logger.info('RESULTS %s', context)
			return render(request, 'attendance/MainHTML/revhome.html/', context)
		
		else:
			raise Exception('Method not allowed')

	except Exception as identifier:
		logger.info('ERROR %s', identifier.args[0])
		context = {
			'error': True,
			'message': 'Hong gan liao unexpected error occured. Please contact your encik for support.'
		}
		return render(request, 'attendance/MainHTML/revhome.html/', context)

def troll_view(request):
	return redirect('https://www.youtube.com/watch?v=xt4hSs4IWPg')

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