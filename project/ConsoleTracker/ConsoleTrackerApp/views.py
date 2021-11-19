from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm
from django.views.generic.list import ListView
from .models import Machine, User, User_uses_machine
import datetime


# Create your views here.

def timer(request, id):
    machine = get_object_or_404(Machine, id=id)
    user = User.objects.get(id=1)
    # set variables
    user_uses_machine = None
    epochTime = 0;
    # Enter the countdown only if the machine is active
    username = "Not In Use"
    if machine.active:
        # if the machine is active get the relationship model with the user
        user_uses_machine = User_uses_machine.objects.get(machine=machine, expired=False)
        user = user_uses_machine.user
        epochTime = user_uses_machine.end_time.timestamp()
        username = user.name
    return render(request, "countdown.html",
                  {"machine": machine, "username": username, "user_uses_machine": user_uses_machine,
                   "epochTime": epochTime})


def time_manager(request, id):
    # get machine and user objects
    machine = get_object_or_404(Machine, id=id)
    user = User.objects.get(id=1)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # make sure machine is not already active
        if not machine.active:
            # if the machine is not active add the user and the machine to the relationship model
            User_uses_machine.objects.create(user=user, machine=machine)
        # redirect to timer countdown page
        return HttpResponseRedirect('/timer/' + str(id))
    else:
        # convert the time to hh:mm:ss and send to template
        timeLeft = str(datetime.timedelta(seconds=user.time))
    return render(request, "time_manager.html", {"machine": machine, "user": user, "timeLeft": timeLeft})


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
            return HttpResponseRedirect('/machines')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, "login.html", {'form': form})


class machines(ListView):
    model = Machine
