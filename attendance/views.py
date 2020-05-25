from django.shortcuts import render
from django.http import HttpResponse
from .models import Trooper, Absence

def homepage(request):
    context = { 

    }
    return HttpResponse("Testicles")

