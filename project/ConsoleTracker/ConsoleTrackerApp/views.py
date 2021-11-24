from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from .models import Machine
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm

# Create your views here.

def timer(request, id):
	username = 'User12345'
	timeLeft = 3000
	Machine_ID = 1
	machine = get_object_or_404(Machine, id=id)
	return render(request, "countdown.html", {"machine": machine, "username": username, "Machine_ID": Machine_ID, "timeLeft": timeLeft})

class machines(ListView):
	model = Machine

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid() and form.validate_login(form.cleaned_data['uname'], form.cleaned_data['pword']):
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/timer')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, "login.html",  {'form': form})
