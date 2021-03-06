from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from attendance.models import Personnel, Absence, Parade
import datetime
import logging
import sys
from django.db import transaction
from .utils import (get_all_personnel, add_personnel, 
edit_personnel, delete_personnel, get_search)

def dashboard_view(request):
	logger = logging.getLogger(__name__)
	try:

		if request.method == 'GET':
			context = {
				'count': len(Personnel.objects.filter(
					is_deleted = False
				)),
				'company': get_all_personnel(),
				'all_personnel_search': get_search(),
			}
			logger.info('RESULTS %s', context)
			return render(request, 'attendance/MainHTML/revdashboard.html/', context)
			
			
		if request.method == 'POST':
			logger.info('POST DATA %s', request.POST)
			action = int(request.POST.get('action'))
			logger.info('ACTION %s', action)

			name = request.POST.get('personName')
			rank = request.POST.get('personRank')
			platoon = request.POST.get('personPlatoon')
			personnel_id = request.POST.get('personID')
			logger.info('NAME: %s', name)
			logger.info('RANK: %s', rank)
			logger.info('PLT: %s', platoon)
			logger.info('ID: %s', personnel_id)

			if action == 0:
				# add personnel
				# transaction.set_autocommit(False)
				try:
					add_personnel(name,rank,platoon)
				except Exception as identifier:
					# transaction.rollback()
					raise Exception(identifier.args[0])
				# transaction.commit()
				# return render(request, 'attendance/MainHTML/revdashboard.html/', context)
				return HttpResponseRedirect(
					request.path_info)
			
			elif action == 1:
				# edit personnel
				transaction.set_autocommit(False)
				try:
					edit_personnel(personnel_id, name,rank,platoon)
				except Exception as identifier:
					transaction.rollback()
					raise Exception(identifier.args[0])
				transaction.commit()
				return HttpResponseRedirect(
					request.path_info)
			
			elif action == 2:
				# delete personnel
				transaction.set_autocommit(False)
				try:
					delete_personnel(personnel_id)
				except Exception as identifier:
					transaction.rollback()
					raise Exception(identifier.args[0])
				transaction.commit()
				return HttpResponseRedirect(
					request.path_info)

	except Exception as identifier:
		logger.info('ERROR %s', identifier.args[0])
		context = {
			'error': True,
			'message': 'Hong gan liao unexpected error occured. Please contact your encik for support.'
		}
		return render(request, 'attendance/MainHTML/revdashboard.html/', context)


