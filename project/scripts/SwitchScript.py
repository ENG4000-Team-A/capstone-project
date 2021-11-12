import asyncio
import time
from kasa import SmartPlug
from kasa import Discover
#
#call this function fo find all the ips and switch names in found_devices.items()
async def findDevices():
    found_devices = asyncio.run(Discover.discover())
    return found_devices

#call this function with the the state you want the switch in and its ip to turn off/on the switch
async def ConsolSwitch(state,IP):
    plug = SmartPlug(IP)
    try:
        if(state==1):
            await plug.turn_on()
            return "plug On"
        elif(state==0):
            await plug.turn_off()
            return "plug Off"
        else:
            return "failer"
    except:
        print("Failer to communicate")
