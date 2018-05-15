# Polyphonic Sampled-Sound Synthesizer
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/amaurilopez90/SampledSoundSynth/master/LICENSE)

ADD SYNTH IMAGE HERE

# Abstract
In music production, being able to produce sounds originating from a wide variety of instruments as a strategy to attract the listener and to create 
pieces that would otherwise be played and recorded through live performance is very important. This project aims to recreate such a music synthesizer
that uses sampled sounds as WAV files downloaded from the internet and wave manipulation algorithms to remodel these sounds to desired outputs, using
a raspberry pi as the base computational platform and keys built onto a breadboard to model a launch pad for synthesis.

# How It Works
**Process:**
The user is first able to create their own keyboard using the GPIO button presses on the soundboard created, and then the synthesizer defines
a range of values representing the amount of semi-tone shifts to create. The sound modulation algorithm will then manipulate the sample to generate the
appropriate adapted sampled sound (.wav) files based on the range of semitones. Each of these semitones is a factor of the original sounds frequency 
represented by: **2^(n/12)**, where n represents the semitone shift. The newly generated sounds are then mapped to the user defined keyboard to which the corresponding sound(s) will be output.

**Specifications:**
  1. The device will have two sets of 12 keys. One set will have an original data sample of one instrument while the other set will have a different sample for a different instrument.
     The goal for this is to be able to play at least an octave on each instrument. We see later that manipulating configuration files will allow you to play any number of sounds mapped to any
     GPIO, given that each sound fits onto a corresponding GPIO input pin
     
  2. Sound files used are of .WAV audio file compression, with **16-bit** depth and standard **44.1K** sampling rate
  3. User will be able to play several two or three note chords - synthesizer is **Polyphonic** in nature
  4. Implements the **Phase Vocoder** for sound modulation
  
**Hardware:**
  1. Raspberry Pi 3 Model B
  2. Custom Soundboard with 24 tactile push buttons
  3. HDMI cable to Monitor used for audio output
  
ADD BLOCK DIAGRAM IMAGE HERE

# Theory of Modulation
Each sample needed to exhibit a change in pitch between every button by a factor of 2^(n/12) where n represents the amount of semitone shifts away from the original pitch of the sample. To do this, 
we used the Phase Vocoder which can be split up in the following two parts:

**Time Stretching:**
The idea is to stretch the signal in time while maintaining its original pitch, then changing the speed of playback of that stretched sound by the same factor to result in a pitch shifted sound that
now has the same playback duration as it did originally. In order for the time stretch to work, you first break the sound into windows of overlapping bits.
Then overlapping these bits more or less will shorten and stretch the sound, respectively. 
  
The difficulty regarding these frame overlaps, however, lies within the reconstruction of these frames with one another once the desired overlap has been met. These frames cannot directly be “stitched” 
back together at that point of reconstruction - the two frames do not fit together. In order to fix this discontinuity, some phase transformation needs to take place. In particular, the time stretch method 
computes the phase difference between the two overlapping frames, and looks at the relative shifts in phase to determine how to realign these bins at the boundaries. The steps to do this are as follows:

  1. Window the signal using multiple Hanning Windows of size 2048 samples and a hop size of 256 samples
  2. Analyze two consecutive windows at a time, designated place holders for each
  3. Using the Discrete Fourier Transform (DFT), compute the spectra for each window - spectra1, spectra2
  4. Compute the phase differences between each window pair, insert these into a new phase list, and normalize between values of -pi and pi
  5. Using the Inverse DFT of the magnitudes of spectra2, multiplied by the normalized phase differences, bring all of the amplitudes of the second window back onto the phases of the first window by binding this
     result to the size of the hanning window
  6. Increment each place holder for each window, and repeat steps 2-6 until the entire signal is reconstructed
  
**Pitch Shifting:**
To accomplish a pitch shift, we implement a speed change of the signal - either increasing or decreasing the rate of playback
A speed change by a non-integer factor can be accomplished in the following way:

  1. Create an evenly-spaced array of follows to hold the new .WAV data, with the space being defined by the speed change factor
  2. Repopulate the new .WAV data (that which was the result from the Time Stretch) to hold only values neighboring those in the evenly-spaced array
     EX: If the speed change factor was large, then more space would exist between values in the spaced array, and thus less values would be witheld from the .WAV data.
     With less values present in the .WAV data, the rate of playback would increase, and therefore the pitch observed would also increase.

# Dependencies
  1. PyGame 1.9.4 -> https://www.pygame.org/docs/
  2. PySoundFile 0.9.0 and all associated dependencies -> https://pysoundfile.readthedocs.io/en/0.9.0/
  3. NumPy and SciPi packages and all associated dependencies -> https://docs.scipy.org/doc/
  4. Python 2.7 or later (PiImplementation), Python 3 (PCImplementation)
  
# Installation
  1. Clone this repository using: **git clone**
  2. Configure Raspberry Pi to accept GPIO input, map buttons on breadboard to pins of choice
  3. Run python main.py
  
# Improvements to be made
Some things that should be added is the ability for the user to select which .WAV file(s) (currently present in "samples") that is used for the synthesizer.
Recommend creating some sort of user interface to do this. For now, user must edit Main.py to configure sound objects based off of file locations.
To support multiple sound files used at once, the user must edit configuration files generated to hold more than one sound. To get this to work automatically with
a user interface, I suggest using a method that will merge two or more generated "soundfonts" folders to one "bigSoundFonts" folder, that will then be passed to create the config files
