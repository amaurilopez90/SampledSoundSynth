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

# => Filename: testmixer.py
# => Definition: mixer()
# => Description: This definition sets up the main "mixer" for the synthesizer. It opens up a pygame input interface to begin reading
#                 the user's key presses and outputs the corresponding wav file mapped to those keys in the configuration file. This holds
#                 the main loop of the program to detect push button events and play sounds.
# => Parameters: 
#           - conf_file: Input configuration file
#           - fadeout_time: Amount of time it takes for each sound to fadeout once key press is released  
# => Precondition: Assumes that conf_file is a valid configuration file that was created using the "make_conf" definition
#                  in tools.py. Current implementation also assumes that the currently used device is a user's laptop, NOT the raspberry pi...yet.
# => Postcondition: Returns an events list that documents at which time each sound event had taken place.  

# => Last Data modified on: 4/29/2018
# 
# #####################################################################################################
import pygame, sys
from tools import *
import csv
import time
import RPi.GPIO as GPIO
from gpioSetUp import *

SAMPLE_WIDTH = 16
FPS = 44100
N_CHANNELS = 2
BUFFER = 2**10

pins = {2,3,4,17,27,22,10,9,11,5}
def mixer(conf_file, fadeout_time = 50):
        print("Starting up the Mixer...\n")

	#Opens up a interface that lets you press the keys of your keyboard to play the wavfiles
	#as specified by the conf_file

	#Returns a list of the (time, events) 
	

	pygame.mixer.pre_init(FPS,-SAMPLE_WIDTH,N_CHANNELS,BUFFER)
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((640,480))

	#Read the conf_file
        print("Reading the conf file...\n")

	#Hold the mappings between keys and sounds aswell as keys and files
	keysoundpair = {} 
	keyfilepair = {} 

	#open config file and read line by line
	with open(conf_file, 'r') as f:
		#content = f.readlines()
		content = csv.reader(f, delimiter=',')

		for line in content: #isolate key and wavfile from each other
			if line == "\n":
				continue

			key = line[0]
			wavfile = line[1]
			wavfile = wavfile.strip(" ")
			wavfile = wavfile.strip("\n")
		
			# key, wavfile = key.strip(' '), wavfile.strip(' ')
			if key is not '#':
				print(wavfile)
				keyfilepair[key] = wavfile
				keysoundpair[key] = pygame.mixer.Sound(file=wavfile)
		

	events_list = []

	#reinstate the pin events for event detection
        print("Adding events GPIO....\n")
	addEventsGPIO(pins)

        print("Entering Main Loop, start playing.... \n")
	while True:
		channel, edge = waitForEventChannel()

                print(channel+"\n")
		#check if event is in the list of buttons recorded in config file
		if channel in keysoundpair:
			#find out if it is a rising or falling edge
			if edge == "FALLING":
				keysoundpair[channel].play()

				events_list.append((time.time(), keyfilepair[channel]))

			elif edge == "RISING":
				keysoundpair[channel].fadeout(fadeout_time)
		elif channel == "2": #escape pin, exit program
			break


        print("Removing events GPIO...\n")
	removeEventsGPIO(pins)
	pygame.quit()
	return events_list
