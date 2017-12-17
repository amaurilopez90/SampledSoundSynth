####################################################################################################
""" 
=> Contributors: Amauri Lopez, Darrien Pinkman
=> Course: Senior Project I
=> Semester: Fall 2017
=> Advisor: Dr. Anthony Deese
=> Project name: Polyphonic Sampled Sound Synthesizer 
=> Description: This project aims to recreate such a music synthesizer that uses sampled sounds as
                WAV files downloaded from the internet and wave manipulation algorithms to remodel
                these sounds to desired outputs, using a raspberry pi as the base computational platform
                and keys built onto a breadboard to model a launchpad for synthesis. 

=> Filename: wavFile.py
=> Description: This file holds the WavFile class and the corresponding methods for calculating the 
                .WAV file's original frequency, the closest note represented by that frequency, the sampling rate,
                channels, and .WAV data.


=> Last Data modified on: 12/16/2017
"""
#####################################################################################################
import soundfile as sf
import numpy as n
from numpy.fft import rfft
from numpy import argmax, mean, diff, log
from matplotlib.mlab import find
from scipy.signal import blackmanharris, fftconvolve
from parabolic import parabolic
from noteDictionary import get_note_dict
from time import time

class WavFile():

	notes_dictionary = get_note_dict() #get dicitonary of notes

	#############################################################################################################################
	"""
	=> Definition: __init__()
	=> Description: Serves as the class constructor for the WavFile Class
	=> Parameters: 
	=>        - filepath: filepath for the input wav file 
	"""
	############################################################################################################################
	def __init__(self, filepath):
		
		self.filepath = filepath
		self.name = filepath.split("samples/")[1].split(".wav")[0]
		self.data, self.samplerate = sf.read(filepath)

		#if the sample format is Stereo, then this seems to only work if I convert it to mono first, then get the frequency
		try:
			self.frequency = WavFile.get_freq_from_fft(self.data, self.samplerate)
			self.mono = True
		except Exception as e:
			self.data = self.data.sum(axis=1) / 2 #convert data from stereo to mono
			self.frequency = WavFile.get_freq_from_fft(self.data, self.samplerate)
			self.mono = False

		self.closest_note = min(WavFile.notes_dictionary, key = lambda v: abs(WavFile.notes_dictionary[v] - self.frequency))

	####################################################################################
	"""
	=> Definition: get_freq_from_crossings()
	=> Description: This function counts the zero crossings of the .WAV and divides it
	                  by the average period to get the frequency
	=> Parameters: 
	=>        - data: numpy array representing the sample data of the .WAV file
	            - samprate: the sampling rate of the .WAV file
	 
	=> Precondition: Assumes that the input data is of a valid WavFile object
	=> Postcondition: Returns the estimated frequency of the wav         
	"""     
	####################################################################################
	def get_freq_from_crossings(data, samprate):
		#Count zero crossings, divide average period by time ot get frequency

		# Find all indices right before a rising-edge zero crossing
	    indices = find((data[1:] >= 0) & (data[:-1] < 0))

	    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
	    # crossings = indices

	    # More accurate, using linear interpolation to find intersample
	    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
	    crossings = [i - data[i] / (data[i+1] - data[i]) for i in indices]

	    # Some other interpolation based on neighboring points might be better.
	    # Spline, cubic, whatever

	    return samprate / mean(diff(crossings))

    ####################################################################################
	"""
	=> Definition: get_freq_from_fft()
	=> Description: This function estimates the frequency from the peak of FFT
	=> Parameters: 
	=>        - data: numpy array representing the sample data of the .WAV file
	            - samprate: the sampling rate of the .WAV file
	 
	=> Precondition: Assumes that the input data is of a valid WavFile object
	=> Postcondition: Returns the estimated frequency of the wav         
	"""     
	####################################################################################
	def get_freq_from_fft(data, samprate):
	    #Estimate frequency from peak of FFT   

	    # Compute Fourier transform of windowed signal
	    windowed = data * blackmanharris(len(data))
	    f = rfft(windowed)

	    # Find the peak and interpolate to get a more accurate peak
	    i = argmax(abs(f))  # Just use this for less-accurate, naive version
	    true_i = parabolic(log(abs(f)), i)[0]

	    # Convert to equivalent frequency
	    return samprate * true_i / len(windowed)  

    ####################################################################################
	"""
	=> Definition: get_info()
	=> Description: This function prints of information of the .WAV file 

	=> Precondition: Assumes that the sender is a valid WavFile object
	=> Postcondition: Prints out the information of the .WAV file such as:
		              . The name of the file
		              . The file Format (mono or stereo)
		              . Samplerate
		              . Number of samples
		              . Sample length
		              . Frequency
		              . Closest not to frequency         
	"""     
	####################################################################################
	def get_info(self):
		if self.mono:
			fileformat = "Mono"
		else:
			fileformat = "Stereo"
		length = len(self.data)/self.samplerate
		print("--------------------------------------")
		print("Name: " + self.name)
		print("Format: " + fileformat)
		print("Samplerate: " + str(self.samplerate))
		print("# of Samples: " + str(len(self.data)))
		print("Sample Length: " + str(length) + "s")
		print("Frequency: " + str(self.frequency))
		print("Closest Note: " + self.closest_note)
		print("--------------------------------------")