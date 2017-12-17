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

# => Filename: main.py
# => Description: This file creates the wav objects from wavfiles to be used when creating the user's 
#                 keyboard, the folder of samples generated for that keyboard, and the config file
#                 for the device that maps each wav to a key. It then calls the testmixer file to start the
#                 mixer with the config.

# => Last Data modified on: 12/16/2017

# #####################################################################################################

from wavFile import *
from testmixer import *
from tools import *
from wavManipulation import *
#wav = WavFile("../samples/Dog-Bark.wav")
wav = WavFile("../samples/Alesis-Fusion-Nylon-String-Guitar-C4.wav")
#wav = WavFile("../samples/1980s-Casio-Celesta-C5.wav")
#wav = WavFile("../samples/1kHz_44100Hz_16bit_05sec.wav")
#wav = WavFile("../samples/Bass-Drum-1.wav")

keyboard = make_keyboard("../keyboards/samplekeyboard2.txt") #create a new keyboard called "samplekeyboard2"
samples = note_scaling(wav.data, wav.samplerate, '../samples/soundfonts/'+ wav.name, range(-13, 13))

conf_file = make_conf(samples, "../configs/testconfigwav1scaled.conf", keyboard) #make configuration file called testconfforsamples.conf in configs, and input the keyboard to it. Folder of samples to use is "samples"

#wav.get_info()
mixer(conf_file) #start up the mixer with conf file



