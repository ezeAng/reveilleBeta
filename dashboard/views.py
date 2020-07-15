from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from attendance.models import Personnel, Absence, Parade
import datetime
import logging
import sys
from django.db import transaction
# from .utils import 

def dashboard_view(request):

	if request.method == 'GET':
		context = {
			
		}
	return render(request, 'attendance/MainHTML/revdashboard.html/')