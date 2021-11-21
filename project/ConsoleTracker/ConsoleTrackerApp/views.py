from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Machine

# Create your views here.

def timer(request, id):
	username = 'User12345'
	timeLeft = 3000
	Machine_ID = 1
	machine = get_object_or_404(Machine, id=id)
	return render(request, "countdown.html", {"machine": machine, "username": username, "Machine_ID": Machine_ID, "timeLeft": timeLeft})

class machines(ListView):
	model = Machine