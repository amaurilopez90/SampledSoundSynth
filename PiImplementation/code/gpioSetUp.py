import RPi.GPIO as GPIO

def setUpGPIO(pins):
	#set up pins
	GPIO.setmode(GPIO.BCM)

	for pin in pins:
		GPIO.setup(pin, GPIO.IN)

def addEventsGPIO(pins):
	for pin in pins:
		GPIO.add_event_detect(pin, GPIO.BOTH, callback = myCallback)

def removeEventsGPIO(pins):
	for pin in pins:
		GPIO.remove_event_detect(pin)

def myCallback(pin):
    print("%d was pressed ", pin)




