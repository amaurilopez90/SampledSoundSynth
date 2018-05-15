# ####################################################################################################
# 
# => Contributors: Amauri Lopez, Darrien Pinkman
# => Course: Senior Project I
# => Semester: Fall 2017
# => Advisor: Dr. Anthony Deese
# => Project name: Polyphonic Sampled Sound Synthesizer 
# => Description: This project aims to recreate such a music synthesizer that uses sampled sounds as
#                 WAV files downloaded from the internet and wave manipulation algorithms to remodel
#                 these sounds to desired outputs, using a raspberry pi as the base computational platform
#                 and keys built onto a breadboard to model a launchpad for synthesis. 

# => Filename: gpioSetUp.py
# => Description: This module holds the necessary methods to setup, add, remove, and check for GPIO
#				  events 

# => Last Data modified on: 12/2/2017
# 
# #####################################################################################################

import RPi.GPIO as GPIO

######################################################################################
""" 
=> Definition: setUpGPIO()
=> Description: This function sets up all the GPIO pins specified by the user on the Raspberry Pi as GPIO.IN using set mode BCM 
=> Parameters: 
=>       - pins: a list containing the GPIO pin numbers as labelled on mode BCM
=> Precondition: Assumes that the input is a valid list of positive integers only, and that each integer is not arbitrary and represents
=>               a physical pin on the Raspberry Pi 3 Model B         
"""
######################################################################################
def setUpGPIO(pins):
	#set up pins
	GPIO.setmode(GPIO.BCM)

	for pin in pins:
		GPIO.setup(pin, GPIO.IN)

######################################################################################
""" 
=> Definition: addEventsGPIO()
=> Description: This function adds event detection methods for each pin in the specified list of pins 
=> Parameters: 
=>       - pins: a list containing the GPIO pin numbers as labelled on mode BCM
=> Precondition: Assumes that the input is a valid list of positive integers only, and that each integer is not arbitrary and represents
=>               a physical pin on the Raspberry Pi 3 Model B         
"""
######################################################################################
def addEventsGPIO(pins):
	for pin in pins:
		GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=400)

######################################################################################
""" 
=> Definition: removeEventsGPIO()
=> Description: This function removes event detection methods for each pin in the specified list of pins 
=> Parameters: 
=>       - pins: a list containing the GPIO pin numbers as labelled on mode BCM
=> Precondition: Assumes that the input is a valid list of positive integers only, and that each integer is not arbitrary and represents
=>               a physical pin on the Raspberry Pi 3 Model B. Also assumes that each pin has an event already added by the addEventsGPIO()         
"""
######################################################################################
def removeEventsGPIO(pins):
	for pin in pins:
		GPIO.remove_event_detect(pin)

######################################################################################
""" 
=> Definition: waitForEventChannel()
=> Description: This function waits for a GPIO events to be triggered and prints out which event was detected 
=> Parameters: 
=>       - pins: a list containing the GPIO pin numbers as labelled on mode BCM
=> Precondition: Assumes that the input is a valid list of positive integers only, and that each integer is not arbitrary and represents
=>               a physical pin on the Raspberry Pi 3 Model B         
=> Postcondition: Returns the channel corresponding to the GPIO pin that has triggered the event, along with whether or not the pin event
=>                was triggered on a rising or falling edge
"""
######################################################################################
def waitForEventChannel():
	print("Waiting for event channel:\n")
	channel = " "
	edge = " "

	#start to loop indefinately until both channel and edge are detected - wait for event detect
	while(channel == " " or edge == " "): #loop until both channel and edge are populated

		 if GPIO.event_detected(2): #they hit escape
			channel = "2"

		 elif GPIO.event_detected(3):
			channel = "3"
		 elif GPIO.event_detected(4):
	    		channel = "4"

	    	 elif GPIO.event_detected(17):
	    		channel = "17"

	    	 elif GPIO.event_detected(27):
	    		channel = "27"

	    	 elif GPIO.event_detected(22):
	    		channel = "22"
	    	 elif GPIO.event_detected(10):
	    		channel = "10"

	    	 elif GPIO.event_detected(9):
	    		channel = "9"

	    	 elif GPIO.event_detected(11):
	    		channel = "11"

	    	 elif GPIO.event_detected(5):
	    		channel = "5"

        	 if(channel != " "):
			if(GPIO.input(int(channel))==0):
		        	edge = "FALLING"
			else:
				edge = "RISING"

	print(str(channel) + "\n")
	return str(channel), edge




