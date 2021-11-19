from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Machine

# Create your views here.

def timer(request):
	username = 'User12345'
	timeLeft = 3000
	Machine_ID = 1
	return render(request, "countdown.html", {"username": username, "Machine_ID": Machine_ID, "timeLeft": timeLeft})

class machines(ListView):
	model = Machine