import time
from RPi import GPIO
#TODO: should we import this or embed it?
from gpiozero import MCP3008

# This works with a switch+potentiometer (on/off + volume)


GPIO.setmode(GPIO.BCM)
#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = None

GPIO.setup(26, GPIO.IN)

pot = MCP3008(0)#wired to channel 0
volume = 0
newVolume = 0

while True:
    #take a reading
    input = GPIO.input(26)
    #if the last reading was low and this one high, print
    if (prev_input == None):
        if not input:
            print("starting in on")
        else:
            print("starting in off")
    elif prev_input!= input :
        if not input:
            print("Turned on")
        else:
            print("Turned off")
    #update previous input
    prev_input = input


    if (pot.value < 0.002):
        newVolume = 0
    else:
        newVolume = round(pot.value,2)

    if (volume != newVolume and abs(newVolume - volume)>0.02):
        volume = newVolume
        print(" volume ", volume)

    #slight pause to debounce
    time.sleep(0.1)

