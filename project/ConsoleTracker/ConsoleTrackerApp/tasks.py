from .models import Machine, User_uses_machine, User
from .scripts.SwitchScript import ConsoleSwitch
from .InternalSocketConnect import InternalSocket
from .notifications import sendSMS, NOTIF_TIMES
from threading import Thread
from django.utils import timezone
import asyncio
import time
from kasa import Discover
import sys
# Period in seconds in between syncing switches to machine state
SYNC_PERIOD = 10

# runs kasa functions in another background thread
def switch_off(ip):
    t = Thread(target=ConsoleSwitch, args=(0, ip,))
    t.start()


def switch_on(ip):
    t = Thread(target=ConsoleSwitch, args=(1, ip,))
    t.start()


# runs the update time function
def update_time(socket, username, time):
    return socket.update_time(username, time)


# Updates a users time upon request form opus
def update_user_time(username, new_time):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    # Update the user time if exists
    if user is not None:
        user.time = new_time
        user.save()

        # Updating running timer if exists
        active_timer = None
        try:
            active_timer = User_uses_machine.objects.get(user=user, expired=False)
        except Exception as e:
            return
        # Current left time
        delta = (active_timer.end_time - timezone.now()).total_seconds()
        
        # Adjust time if needed
        time_diff = abs(delta-new_time)
        if delta < new_time: # need to extend timer
            active_timer.end_time += timezone.timedelta(seconds=time_diff)
            active_timer.init_Balance += time_diff
            
        elif delta > new_time: # need to reduce timer
            active_timer.end_time -= timezone.timedelta(seconds=time_diff)
            active_timer.init_Balance -= time_diff

        else: # unchanged
            pass
        active_timer.save()
        return True
    return False


# Ping all machines in the system
def ping_all_machines():
    return list(Machine.objects.all())


# thread to update the time balance of the user
def update_time_thread(socket, now):
    # represents the seconds on the clock we will update time
    check_seconds = [00, 15, 30, 45]
    interval = 15

    # The current system time and the seconds of the current clock
    curr_time = now
    clock_second = int(curr_time.strftime('%S'))

    # print(f"{curr_time.strftime('%S')} {clock_second in check_seconds}", end="\r")

    # if the current clock second is equal to one of the interval times update users' time
    if clock_second in check_seconds:
        # queries for all active machines
        active_machines = User_uses_machine.objects.filter(
            expired=False
        )
        # print(active_machines)
        # loop through each active machine
        for machine in active_machines:
            # determine the seconds between the start of the machine and the current time to figure out if the machine
            # started less than the interval
            start_dif = int((curr_time - machine.start_time).total_seconds())
            # print(f"{curr_time} {machine.start_time}")
            # print(f"{start_dif}")

            if start_dif < interval:
                # If the machine started less than interval update time by difference
                update_time(socket, machine.user.username, start_dif)
                print(f"updating {machine.user.username} time by {start_dif} seconds")
            else:
                # else update by interval
                update_time(socket, machine.user.username, interval)
                print(f"updating {machine.user.username} time by {interval} seconds")


def update_expired_machines(now):
    # like an SQL SELECT where only looking for unexpired timers, from today,
    # with end_time before now
    query_set = User_uses_machine.objects.filter(
        end_time__date=now.date(),
        end_time__time__lte=now.time(),
        expired=False)
    for query in query_set:
        # using end_time since this is a natural ended imer
        stop_timer(query, query.end_time)
        print(query.user.username + ' on ' + query.machine.name + ' ended at '
              + query.end_time.strftime("%m/%d/%Y, %H:%M:%S") + ', set to inactive')


def query_time():
    i = 0
    # create the socket that connects to ExternalSocket
    socket = InternalSocket()

    while True:
        # syncing timezone.now between all functions called here
        now = timezone.now()
        update_time_thread(socket, now)
        send_notifications(now)
        # like an SQL SELECT where only looking for unexpired timers, from today,
        # with end_time before now
        update_expired_machines(now)
        if i >= SYNC_PERIOD:
            i = 0
            t = Thread(target=sync_switch_states)
            t.start()
        i += 1
        # minimum 1 second between loops, but usually 1.01s on my machine.
        # may need to change value to guarantee 1s between loops
        time.sleep(1)


def sync_switch_states():
    """
    Syncs smart switches to match the Machine states.
    Also adds any kasa plugs on network to database,
    or updates database when IP is incorrect.
    """
    devices = asyncio.run(Discover.discover())  # Scan for devices
    for addr, dev in devices.items():  # addr is ip address, dev is SmartDevice
        if dev.is_plug:
            try:
                m = Machine.objects.get(mac=dev.mac)  # try to get matching row in table
                if m.ip != addr:  # correcting IP if it's old/wrong
                    m.ip = addr
                    m.save()
                    print("IP for " + m.name + " changed to " + str(addr))
                else:  # matching switch states to machine states
                    if dev.is_on and not m.active:
                        asyncio.run(dev.turn_off())
                        print("Shutting down machine with ip: {ip}".format(ip=addr))
                    elif not dev.is_on and m.active:
                        asyncio.run(dev.turn_on())
                        print("Powering on machine with ip: {ip}".format(ip=addr))
                    # else:
                    # print("State okay")
            except:
                Machine.objects.create(name=dev.alias, mac=dev.mac, ip=addr)  # add new row
                print('New machine: "' + dev.alias + '" added.')


def send_notifications(now):
    active_machines = User_uses_machine.objects.filter(
        expired=False
    )
    # loop through each active machine
    for machine in active_machines:
        # looks for valid format phone number without country calling code
        if len(machine.user.phone_number) == 10:
            # country code for Canada and US, will need proper way to get for other countries
            country_code = "+1"
            timer = int((machine.end_time - now).total_seconds())
            if timer in NOTIF_TIMES:
                msg = str(int(timer / 60)) + " minutes remaining on " + machine.machine.name + "."
                msg += '\nPlease use website for accurate timer.'
                # print('sending sms')
                t = Thread(target=sendSMS, args=(country_code + machine.user.phone_number, msg,))
                t.setName('SMS')
                t.start()
                
def stop_timer(active_timer :User_uses_machine, now):
    """
    Sets endtime of an active timer to now.
    Sets users time to remaining timer value.
    """
    """
    new_endtime = timezone.now()
    delta = active_timer.end_time - new_endtime
    active_timer.end_time = timezone.now() + delta
    active_timer.start_time = timezone.now()
    active_timer.save()
    active_timer.user.time = delta.total_seconds()
    active_timer.user.save()
    """
    print("Start time = {st}, Endtime = {et}, Initial Balance = {eb}".format(st=active_timer.start_time,
                                                                             et=active_timer.end_time,
                                                                             eb=active_timer.init_Balance))
    new_endtime = now
    print("New Endtime = {nt}".format(nt=new_endtime))
    active_timer.end_time = new_endtime
    active_timer.expired = True
    delta = (new_endtime - active_timer.start_time).total_seconds()
    print("Time Used = {tu}".format(tu=delta))
    active_timer.user.time = max(0, active_timer.init_Balance - delta)
    print("New Balance = ", active_timer.user.time)
    active_timer.machine.active = False

    active_timer.save()
    active_timer.user.save()
    active_timer.machine.save()
    switch_off(active_timer.machine.ip)


def start_query_daemon():
    """runs query_time in a background thread"""
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith(
            'win'):  # windows bug https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    t = Thread(target=query_time)
    t.daemon = True
    t.start()
