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

# => Filename: tools.py
# => Description: This file holds all the tools necessary to put together the synthesizer. This "toolbox"
#                 includes the methods to create keyboard text files that contain the keys pressed by the user
#                 to outline their keyboard, read the created keyboard text files, and create the configuration files
#                 that holds the mappings between the keys and their corresponding .WAV files   

# => Last Data modified on: 12/16/2017
# 
# #####################################################################################################

import pygame
import csv
import os
import shutil

######################################################################################
"""
=> Definition: make_keyboard()
=> Description: This definition opens an interactive sessoin that lets you hit the keys of
                your keyboard in the desired order. This definition saves the input into a text
                file at the file location specified. Press escape the finish
=> Parameters: 
=>       - outputfile: Filepath in which the keyboard textfile will be saved to 

=> Postcondition: Creates a file to the specified location by outputfile, containing the keys
                  input by the user for their keyboard         
"""     
######################################################################################
def make_keyboard(outputfile):
    
    txt_file = open(outputfile, 'w')
    
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            else:
                name = pygame.key.name(event.key)
                print (name)
                txt_file.write(name + '\n')
    txt_file.close()
    pygame.quit()
    return outputfile

######################################################################################
"""
=> Definition: read_keyboard()
=> Description: This definition reads a keyboard file and returns a list of keys
=> Parameters: 
=>       - txt_file: Filepath in which the keyboard textfile will be read from 

=> Precondition: Assumes that the input txt_file exists and is one created using the make_keyboard definition in tools.py
=> Postcondition: Retuns a list of keys read fromt the keyboard text file         
"""     
######################################################################################
def read_keyboard(txt_file):
    
    return [ key.strip('\n').split('|') for key in open(txt_file, 'r')]

######################################################################################
"""
=> Definition: make_conf()
=> Description: This definition creates a configuration file out of a samples folder and an input keyboard file.
                This configuration file holds a mapping between the keys in the keyboard file and the .WAV files in the samples folder
=> Parameters: 
=>       - samplefolder: The input folder holding all of the .WAV or .ogg files to be played on the keyboard
         - output: Filepath in which the configuration file will be saved to
         - keyboardfile: A keyboard text file holding the keys that were earlier pressed by the user when making their keyboard 

=> Precondition: Assumes that the input samplefolder exists. Also assumes that the keyboardfile exists and is one created using the 
                 make_keyboard definition in tools.py
=> Postcondition: Creates a configuration file at the specified output filepath. Returns the name of that filepath         
"""     
######################################################################################
def make_conf(samplefolder, output, keyboardfile, startfile=0):
    
    keyslist = read_keyboard(keyboardfile) #get the keys in a list

    conf_file = csv.writer(open(output, 'w'), delimiter=',')
    files = filter(lambda s : s.endswith(('.wav','.ogg')),
                   os.listdir(samplefolder))
              
    files = sorted(files)[startfile:]
    
    if keyslist is None:
        
        keyslist = len(files) * [['#']]
        
    for name,keys in zip(files,keyslist):
        
        for k in keys:
            
            conf_file.writerow([k,' ' + '%s/%s'%(samplefolder,name)])

    return output

# def merge_two_folders(folder1, folder2, outputfolder):
#     if not os.path.exists(outputfolder):
#         os.makedirs(outputfolder)
        
#     src_files = os.listdir(folder1)
#     for file_name in src_files:
#         full_file_name = os.path.join(folder1, file_name)
#         if (os.path.isfile(full_file_name)):
#             shutil.copy(full_file_name, outputfolder)

#     src_files = os.listdir(folder2)
#     for file_name in src_files:
#         full_file_name = os.path.join(folder2, file_name)
#         if (os.path.isfile(full_file_name)):
#             shutil.copy(full_file_name, outputfolder)