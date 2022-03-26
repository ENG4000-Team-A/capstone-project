import asyncio

from kasa import Discover
from kasa import SmartPlug


# This function discovers all the IP's and switch names
def findDevices():
    found_devices = asyncio.run(Discover.discover())
    return found_devices


#  This function takes in the IP address and state of a switch to then turn it on/off
def ConsoleSwitch(state, IP):
    plug = SmartPlug(IP)
    try:
        if state == 1:
            asyncio.run(plug.turn_on())
            return "plug On"
        elif state == 0:
            asyncio.run(plug.turn_off())
            return "plug Off"
        else:
            return "failer"
    except:
        print("Failed to communicate")
