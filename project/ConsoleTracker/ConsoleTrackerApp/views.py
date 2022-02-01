from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm
from django.views.generic.list import ListView
from .models import Machine, User, User_uses_machine
import datetime
from .tasks import switch_on, switch_off, stop_timer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
import json

# Create your views here.

def timer(request, id):
    machine = get_object_or_404(Machine, id=id)
    user = User.objects.get(id=1)
    # set variables
    user_uses_machine = None
    epochTime = 0
    # Enter the countdown only if the machine is active
    username = "Not In Use"
    if machine.active:
        # if the machine is active get the relationship model with the user
        user_uses_machine = User_uses_machine.objects.get(machine=machine, expired=False)
        user = user_uses_machine.user
        epochTime = user_uses_machine.end_time.timestamp()
        username = user.username
    if request.method == "POST":
        # post request from button pressed
        stop_timer(user_uses_machine)
        # redirects to same page only to show user the change to timer
        return HttpResponseRedirect('/timer/' + str(id))
    else:        
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
            # set users timebalance to 0 
            user.time = 0
            user.save()
            # turns on the switch & set machine to active
            machine.active = True
            machine.save()
            switch_on(machine.ip)           
        # redirect to timer countdown page
        return HttpResponseRedirect('/timer/' + str(id))
    else:
        # convert the time to hh:mm:ss and send to template
        timeLeft = str(datetime.timedelta(seconds=user.time))
    return render(request, "time_manager.html", {"machine": machine, "user": user, "timeLeft": timeLeft})

@csrf_exempt 
def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        body = json.loads(request.body)
        #username = body['uname']
        #password = body['pword']
        form = NameForm(body)
        
        # check whether it's valid:
        if form.is_valid():
            data = form.validate_login(form.cleaned_data['uname'], form.cleaned_data['pword'])
            
            if data is not None:
                # Create a new instance of the user model if the user is not yet on our system
                if data["usernameExists"] and data["validPassword"]:  
                    try:
                        user_exists = User.objects.get(username=data['username'])
                    except User.DoesNotExist:
                        user_exists = None
                    if user_exists is None:
                        new_user = User(username=data['username'], time=data['timeRemaining'],
                                        first_name=data['firstName'], last_name=data['lastName'],
                                        phone_number=data["phoneNumber"])
                        new_user.save()
                    return JsonResponse({"status": 'Successful Login',
                    })
                else:
                    return JsonResponse({"status": 'Credentials not valid'})

                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                # For now it will redirect to the same page after attempted login
                # but now just show the json response for us to observe

        else:
            return JsonResponse({"status": 'Fail: form not valid'}) 
                
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return JsonResponse({"status": 'Fail: Not a POST request'}) 


class machines(ListView):
    model = Machine
