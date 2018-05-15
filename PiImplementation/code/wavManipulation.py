# ####################################################################################################
""" 
# => Contributors: Amauri Lopez, Darrien Pinkman
# => Course: Senior Project I
# => Semester: Fall 2017
# => Advisor: Dr. Anthony Deese
# => Project name: Polyphonic Sampled Sound Synthesizer 
# => Description: This project aims to recreate such a music synthesizer that uses sampled sounds as
#                 WAV files downloaded from the internet and wave manipulation algorithms to remodel
#                 these sounds to desired outputs, using a raspberry pi as the base computational platform
#                 and keys built onto a breadboard to model a launchpad for synthesis. 

# => Filename: wavManipulation.py
# => Description: This file holds all the methods involved with .WAV manipulation, specifically the
#                 methods responsible for changing the speed of the .WAV, Time-Stretching the sound, 
#                 Pitch-shifting the sound, and creating a folder of .WAV files used for playback


# => Last Data modified on: 12/2/2017
# """
# #####################################################################################################
import os
import numpy as n
import soundfile as sf
import sys

######################################################################################
""" 
=> Definition: note_scaling()
=> Description: This function initiates the call to start shifting the pitch of the 
               .WAV file and creates a Sample folder to hold the created pitch-shifted
               .WAV files
=> Parameters:
=>        - input_data: numpy array representing the sample data of the .WAV file
         - input_samp: the sampling rate of the .WAV file
         - outputfolder: desired name of the output folder that is created
         - shifts: array of integers representing the number of shifts to be created.
                   Ex: [-2, -1, 1, 2] will create new .WAV samples pitch-shifted by 
                   2 semitones down, 1 semitone down, 1 semitone up, and 2 semitones up 
=> Precondition: Assumes that the input data is of a valid WavFile object, and shifts is a valid
                range array
=> Postcondition: Creates a folder to the specified location by outputfolder, containing the new .WAV files
                 Returns the name/location of the output folder         
"""
######################################################################################
def note_scaling(input_data, input_samp, outputfolder, shifts):
        print("Beginning to scale notes...\n")
	#folder = os.path.dirname(outputfolder)
	#if parent folder doesn't already exist, make it
	if not os.path.exists(outputfolder):
		os.makedirs(outputfolder)

	for i, s in enumerate(shifts): #get index i and value s in list of shifts
		outputfile = "%s%02d.wav"%(outputfolder + '/', i) #set up the file names for each wav to be created
		transposed = pitch_shift(input_data, s)
		sf.write(outputfile, transposed.astype(input_data.dtype), input_samp)

	return outputfolder

######################################################################################
""" 
=> Definition: change_speed()
=> Description: This function changes the speed of playback of the .WAV file by some factor. This
                accomplishes the shift in pitch. 
=> Parameters: 
=>       - wav_data: numpy array representing the sample data of the .WAV file
         - factor: The factor at which the speed of the sound will be changed. 
=> Precondition: Assumes that the input data is of a valid WavFile object, and that the factor is a real and rational number.
=> Postcondition: Returns a new wav_data array that holds values closest to those spaced out by the input factor         
"""
######################################################################################
def change_speed(wav_data, factor): 
	
	indices = n.round(n.arange(0, len(wav_data), factor)) #create an even-spaced array (wav_data) spaced by the factor. Ex. if factor was 2.333 it would change (1, 2, 3, 4, etc.) to (0, 2.333, 4.666 etc.)
	indices = indices[indices < len(wav_data)].astype(int) #astype int takes the neghboring values to these, but then preserves the same vector length. 
	return wav_data[indices.astype(int)]

######################################################################################
""" 
=> Definition: time_stretch()
=> Description: This function stretches the input .WAV file by an input factor. Stretching the sound while maintaining its pitch
=> Parameters: 
=>       - wav_data: numpy array representing the sample data of the .WAV file
         - factor: The factor at which the duration of the sound will be changed
         - DFT_size: The size of the Discrete Fourier Transform window that will  be applied to the signal
         - hop_size: The corresponding hop sizes between each consecutive frame of the signal 
=> Precondition: Assumes that the input data is of a valid WavFile object, and that the factor is a real and rational number.
                 Also assumes that the DFT_size and hop_size are both represented in bits, and are also both real and rational numbers
                 that are less than the length of the orginal sound.
=> Postcondition: Returns a reconstructed sequence of samples that is scaled to match the original amplitude of the signal at each 
                  sample index.          
"""
######################################################################################
def time_stretch(wav_data, factor, DFT_size, hop_size):
	#stretches the sound by a factor 
	
	L = len(wav_data)
	#set up our signal arrays to hold the processing output
	phi = n.zeros(DFT_size) #create an array of zeros (float) of DFT_size
	out = n.zeros(DFT_size, dtype = complex)
	signal_out = n.zeros(int(L/factor) + DFT_size, dtype = complex)

	#Find out what the peak amplitude of input is (for scaling) and create a hanning window
	amp = max(wav_data)
	hanning_window = n.hanning(DFT_size)

	p = 0
	pp = 0
	while p < L - (DFT_size + hop_size):

		#take the spectra of two consecutive windows
		p1 = int(p)
		spectra_1 = n.fft.fft(hanning_window * wav_data[p1: p1 + int(DFT_size)])
		spectra_2 = n.fft.fft(hanning_window * wav_data[p1 + int(hop_size): p1 + int(DFT_size) + int(hop_size)])

		#take their phase difference and integrate
		phi += (n.angle(spectra_2) - n.angle(spectra_1)) #about aligning two nieghboring spectra, by looking at the relative shifts of phase at each frequency bin - based on their phase difference 
		#determine how to line them up without any discontinuities at the boundaries.

		#bring the phase back between pi and -pi
		for i in phi:
			while i < -n.pi: i += 2*n.pi
			while i >= n.pi: i -= 2*n.pi

		out.real, out.imag = n.cos(phi), n.sin(phi)
		#inverse FFT and overlap-add to reconstruct the sequence
		signal_out[pp:pp+int(DFT_size)] += (hanning_window * n.fft.ifft(n.abs(spectra_2)*out)) #using overlapping and blending - provides a smooth transition between two neighboring windows
		pp += int(hop_size)
		p += hop_size*factor

	#write the output and scale it to match the original amplitude
	signal_out = amp*signal_out/max(signal_out)

	return signal_out

######################################################################################
""" 
=> Definition: pitch_shift()
=> Description: This function begins to change the pitch of the sound by implementing
                the Phase Vocoder method. That is first time-stretching the sound, then 
                speedh changing it all by a common factor.
=> Parameters: 
=>       - wav_data: numpy array representing the sample data of the .WAV file
         - n: The amount of semitones to change the pitch of the signal by 
=> Precondition: Assumes that the input data is of a valid WavFile object, and that n comes from the values
                 inside of a valid range array
=> Postcondition: Returns a new wav_data array that holds values closest to those spaced out by the input factor
                  from the time stretched data array         
""" 
######################################################################################
def pitch_shift(wav_data, n, DFT_size = 2**11, hop_size=2048/8):
	print(len(wav_data))
	#changes the pitch of a sound by n semitones
	factor = 2**(1.0 * n / 12.0)
	stretched = time_stretch(wav_data, 1.0/factor, DFT_size, hop_size)
	#print(stretched)
	return change_speed(stretched[DFT_size:], factor)



