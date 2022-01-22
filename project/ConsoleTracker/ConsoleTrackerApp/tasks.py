from .models import Machine, User_uses_machine
from .scripts.SwitchScript import ConsolSwitch
from threading import Thread
from django.utils import timezone
import asyncio
import time
from kasa import Discover
import sys

# Period in seconds in between syncing switches to machine state
SYNC_PERIOD = 10

# seperated out because nested function calls didnt work
def turn_off_switch_help(ip):
    asyncio.run(ConsolSwitch(0, ip))

def turn_on_switch_help(ip):
	asyncio.run(ConsolSwitch(1, ip))


# runs kasa functions in another background thread
def switch_off(ip):
	t = Thread(target=turn_off_switch_help, args=(ip,))
	t.start()

def switch_on(ip):
	t = Thread(target=turn_on_switch_help, args=(ip,))
	t.start()


def query_time():
    i = 0
    while True:
        # like an SQL SELECT where only looking for unexpired timers, from today,
        # with end_time before now
        query_set = User_uses_machine.objects.filter(
            end_time__date=timezone.now().date(),
            end_time__time__lte=timezone.now().time(),
            expired=False)
        for query in query_set:
            query.machine.active = False
            query.machine.save()
            query.expired = True
            query.save()
            switch_off(query.machine.ip)
            print(query.user.name + ' on ' + query.machine.name + ' ended at '
                  + query.end_time.strftime("%m/%d/%Y, %H:%M:%S") + ', set to inactive')
        # minimum 1 second between loops, but usually 1.01s on my machine.
        # may need to change value to guarantee 1s between loops
        time.sleep(1)
        i += 1
        if i >= SYNC_PERIOD:
            i = 0
            sync_switch_states()


def sync_switch_states():
    """
    Syncs smart switches to match the Machine states.
    """
    print("Checking switch states")
    devices = asyncio.run(Discover.discover()) # Scan for devices
    machines = Machine.objects.all() # Get machines
    for m in machines:
        for addr, dev in devices.items(): # addr is ip address, dev is SmartDevice
            #asyncio.run(dev.update())
            if (m.ip == addr):
                if (dev.is_on and m.active == False ):
                    asyncio.run(dev.turn_off())
                    print("Shutting down machine with ip: {ip}".format(ip=addr))
                elif (not dev.is_on and m.active == True):
                    asyncio.run(dev.turn_on())
                    print("Powering on machine with ip: {ip}".format(ip=addr))
                else:
                    print("State okay")
                    

# runs query_time in a background thread
def start_query_daemon():
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'): # windows bug https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    t = Thread(target=query_time)
    t.daemon = True
    t.start()
