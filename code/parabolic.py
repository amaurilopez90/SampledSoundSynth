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

# => Filename: parabolic.py
# => Definition: parabolic()
# => Description: This definition performs quadratic interpolation for estimating the true position of
#                 an inter-sample maximum when nearby samples are known.
# => Parameters: 
#           - f: Input vector
#           - x: Index for that vector 
# => Precondition: Assumes that f is a dicrete time fourier transform vetor of real input and x is a
#                  less accurate, naive version of the inter-sample maximum
# => Postcondition: Returns the coordinates of the vertex of a parabola that goes through point x and
#                   its two neighbors.
# => Example:
#     Defining a vector f with a local maximum at index 3 (= 6), find local
#     maximum if points 2, 3, and 4 actually defined a parabola.
   
#     In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
   
#     In [4]: parabolic(f, argmax(f))
#     Out[4]: (3.2142857142857144, 6.1607142857142856)  

# => Last Data modified on: 12/2/2017
# 
# #####################################################################################################
def parabolic(f, x):
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)