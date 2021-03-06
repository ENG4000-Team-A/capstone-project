import json

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from .auth import generateToken, getUsernameFromToken
from .forms import NameForm
from .models import Machine, User, User_uses_machine
from .tasks import switch_on, stop_timer


@csrf_exempt
def start_timer(request, id):
    """
    Starts the timer for a user. Should only be a post request.
    Parameters:
        id: Machine id

    Post body Parameters:
        uname: User username
        
    Returns:
        User_uses_machine new object or error message
    """
    if request.method == "POST":
        uname = getUsernameFromToken(request)
        if uname is not None:
            try:
                machine = Machine.objects.get(id=id)
                # data = json.loads(request.body)
                if machine.active:
                    return JsonResponse({'data': "machine already active"})

                user = User.objects.get(username=uname)
                obj = User_uses_machine.objects.create(user=user, machine=machine, init_Balance=user.time)
                # turns on the switch & set machine to active
                machine.active = True
                machine.save()
                switch_on(machine.ip)
                return JsonResponse({'data': model_to_dict(obj)})

            except Exception as e:
                print(e)
                return JsonResponse({'data': str(e)})
        else:
            return JsonResponse({'data': "Invalid Authentication"})

    else:
        return JsonResponse({'data': "only post"})


@csrf_exempt
def timer(request):
    """
    Get current User_uses_machine or Stop timer.

    GET Request:
        Returns User_uses_machine or Error message

    POST Request:
        Parameters:
            action:
                Values: "stop" (for stopping)
    """
    uname = getUsernameFromToken(request)
    if uname is not None:
        try:
            user = User.objects.get(username=uname)
            user_uses_machine = User_uses_machine.objects.get(user=user, expired=False)
            # Enter the countdown only if the machine is active
            if request.method == "POST":
                data = json.loads(request.body)
                if 'action' in data:
                    if data['action'] == "stop":
                        stop_timer(user_uses_machine, timezone.now())
                        return JsonResponse({'data': "stopped"})
                    else:
                        return JsonResponse({'data': "invalid action"})
                else:
                    return JsonResponse({'data': "action was not passed"})
            else:
                # if the machine is active get the relationship model with the user
                return JsonResponse({'data': model_to_dict(user_uses_machine)})
        except Exception as e:
            return JsonResponse({'data': str(e)})
    else:
        return JsonResponse({'data': "Invalid Authentication"})


@csrf_exempt
def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        body = json.loads(request.body)
        # username = body['uname']
        # password = body['pword']
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

                    payload_data = {"username": data['username']}
                    return JsonResponse({"status": 'Successful Login', "authToken": generateToken(payload_data)
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


def getMachines(request):
    mid = request.GET.get('id', None)
    if mid is not None:
        return JsonResponse({'data': model_to_dict(Machine.objects.get(pk=mid))})
    return JsonResponse({'data': list(Machine.objects.all().values())})


def getUsers(request):
    uname = getUsernameFromToken(request)
    if uname is not None:
        try:
            user = User.objects.get(username=uname)
            json = model_to_dict(User.objects.get(username=uname))
            try:  # check if user is using a machine
                timer = User_uses_machine.objects.get(user=user, expired=False)
                machine = timer.machine.name
            except:
                machine = "None"
            json["machine"] = machine
        except Exception as e:
            json = {}
        return JsonResponse({'data': json})
    return JsonResponse({'data': "Invalid Authentication"})


def getUser(request):
    mid = request.GET.get('id', None)
    if mid is not None:
        return JsonResponse({'data': model_to_dict(User.objects.get(pk=mid))})
    return JsonResponse({'data': list(User.objects.all().values())})


class machines(ListView):
    model = Machine


class time(ListView):
    model = User
