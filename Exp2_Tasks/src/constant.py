# coding=utf-8


from psychopy import visual, core, event, monitors, gui, data, hardware
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import pandas as pd
import numpy as np
import random

import datetime
import os
import re
import psychopy.iohub as io
from psychopy.hardware import keyboard

import serial  # for triggers

import pyfiglet
import termcolor

### ------------------------- ADMIN ------------------------- ###

TEST_MODE = 0
GUI_ENABLED = 1
IF_SEE_COMPUTR_PLAY = 0


### ------------------------- TERMINAL ------------------------- ###

def start_terminal():
    os.system('clear')
    message = pyfiglet.Figlet(font='univers').renderText('DACFE')
    print(termcolor.colored(message, 'blue'))


### ------------------------- GUI ------------------------- ###

def GUI(GUI_ENABLED):
    TIME = datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S")

    if GUI_ENABLED:

        import PyQt5  # PyQt5 is a tool for GUI Design

        ### Experimenters ###
        EXPERIMENTERS = ['Yue Zhu', 'Jade Gordon', 'Maya Bruni', 'Dina Furman', 'Ziqi Fu']

        myDlg = gui.Dlg(title='DCFE')
        myDlg.addText(f'Time: {TIME}')
        myDlg.addField('PID*')
        myDlg.addField('PN*')
        myDlg.addField('Age*')
        myDlg.addField('Gender*', choices=['Female', 'Male', 'Other'])  # female male other
        myDlg.addField('Experimenter', choices=EXPERIMENTERS)
        myDlg.addField('Run(1 unless rerun)', 1, tip='1 unless Rerun')

        try:
            PID, PN, AGE, GENDER, EXPERIMENTER, RUN = myDlg.show()
            EXPTR_INITIAL = EXPERIMENTER.split()[0][0] + EXPERIMENTER.split()[1][0]
        except:
            message = 'Session Cancelled \n Please restart the program.'
            raise Exception(termcolor.colored(message, 'red'))

        try:
            PN = int(PN)
        except:
            message = 'The entered PID is NOT a number \n Please restart the program.'
            raise Exception(termcolor.colored(message, 'red'))
        try:
            AGE = int(AGE)
        except:
            message = 'The entered AGE is NOT a number \n Please restart the program.'
            raise Exception(termcolor.colored(message, 'red'))
        try:
            RUN = int(RUN)
        except:
            message = 'The entered Run is NOT a number \n Please restart the program.'
            raise Exception(termcolor.colored(message, 'red'))

    else:
        PID, PN, AGE, GENDER, RUN, EXPTR_INITIAL = [np.random.randint(1, 1000), np.random.randint(1, 1000), 999, 'O', 'AI']

    expInfo = {'PID': PID, 'PN':PN, 'Age': AGE, 'Gender': GENDER, 'Run': RUN,
               'TIME': TIME, 'EXPERIMENTER': EXPTR_INITIAL}

    return expInfo


### ------------------------- RUN SET UP  ------------------------- ###

start_terminal()
EXPINFO = GUI(GUI_ENABLED)
PID = EXPINFO.get('PID')
PN = EXPINFO.get('PN')
SONA = EXPINFO.get('SONA')
RUN = EXPINFO.get('Run')
try:
    os.mkdir(f'.{os.sep}data{os.sep}{PID}')  # make a directory for each participant
except:
    print('It seems like you are running the same participant more than once. Be careful about the data!')
FILENAME = f'.{os.sep}data{os.sep}{PID}{os.sep}{PID}_task'
EXPDATA = data.ExperimentHandler(dataFileName=FILENAME,
                                 extraInfo=EXPINFO,
                                 saveWideText=True)  # save as .csv file


### ------------------------- PSYCHOPY ------------------------- ###

### Window Setup ###
WIN = visual.Window(
    size=[1280, 1024],
    fullscr=True,  # not run in full screen when debugging
    color='black',
    screen=0,
    allowGUI=True,
    allowStencil=True,
    monitor='testMonitor',
    units='height',  # relative to the percentage of the screen # NOTE: visual angle available, see psychopy page
    colorSpace='rgb255')  # ??? LATER SOMETHING IS OFF WITH THE COLOR SCALE
# store frame rate of monitor if we can measure it
EXPINFO['frameRate'] = WIN.getActualFrameRate()
if EXPINFO['frameRate'] is not None:
    frameDur = 1.0 / round(EXPINFO['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

WIN.mouseVisible = False

### Set Up Keyboard & Mouse ###
KB = keyboard.Keyboard()
MS = event.Mouse()


### ------------------------- --------- ------------------------- ###
### -------------------------  TRIGGER  ------------------------- ###
### ------------------------- --------- ------------------------- ###

P_TRIG  = f'.{os.sep}stimuli{os.sep}trigger{os.sep}DACFE_trigger.csv'
DF_TRIG = pd.read_csv(P_TRIG)

SER = serial.Serial('COM3', 115200, timeout=0)
if SER.isOpen() == False: SER.open() # open the serial port only if not open yet

# send for 0.01 seconds
def sendTrigger(ser, i, keep=0.01):
        """
        Send a trigger of specified integer value.
        See this link for help: http://web.cecs.pdx.edu/~harry/compilers/ASCIIChart.pdf.

        @i: integer value for a trigger

        (ser has to be a global variable)
        """
        i = int(i)
        # print(type(i)) # debug
        trigger = format(i, '02x').upper().encode()  # format把trigger code编码为两位的16进制字符; encode格式为UTF-8
        # print(trigger)
        ser.write(trigger)
        ser.flush()
        core.wait(keep)
        ser.write('00'.encode())
        ser.flush()

# start sending until end
def startTrigger(ser, i):
    """
    Turn on a trigger using an integer value
    See this link for help: http://web.cecs.pdx.edu/~harry/compilers/ASCIIChart.pdf.

    @i: integer value for a trigger

    (ser has to be a global variable)
    """
    i = int(i)
    # print(type(i)) # debug
    trigger = format(i, '02x').upper().encode()
    # print(trigger)
    ser.write(trigger)
    ser.flush()

# end sending
def endTrigger(ser):
    """
    Turn off all triggers

    (ser has to be a global variable)
    """
    ser.write('00'.encode())
    ser.flush()


### ------------------------- --------- ------------------------- ###
### ---------------------- Task Constants ----------------------- ###
### ------------------------- --------- ------------------------- ###

### Instruction Path ###
INST_PATH = f'.{os.sep}instructions{os.sep}'
INST_BEGIN = f'{INST_PATH}inst_begin{os.sep}'
INST_PRAC_2 = f'{INST_PATH}inst_prac_2{os.sep}'
INST_TO_CALI = f'{INST_PATH}inst_to_cali{os.sep}'
INST_CALI = f'{INST_PATH}inst_cali{os.sep}'  # Only practice 2-back before calibration
INST_PRAC_1 = f'{INST_PATH}inst_prac_1{os.sep}'
INST_PRAC_1_NEXT = f'{INST_PATH}inst_prac_1_next{os.sep}'
INST_PRAC_3 = f'{INST_PATH}inst_prac_3{os.sep}'
INST_PRAC_3_NEXT = f'{INST_PATH}inst_prac_3_next{os.sep}'
INST_PRAC_main = f'{INST_PATH}inst_prac_main{os.sep}'
INST_PRAC_end = f'{INST_PATH}inst_prac_end{os.sep}'
INST_LEARNING = f'{INST_PATH}inst_learning{os.sep}'
INST_OFFLINE_RATING_T0 = f'{INST_PATH}inst_offline_rating_0{os.sep}'
INST_OFFLINE_RATING_T1 = f'{INST_PATH}inst_offline_rating_1{os.sep}'
INST_OFFLINE_RATING_T2 = f'{INST_PATH}inst_offline_rating_2{os.sep}'
INST_OFFLINE_RATING_T3 = f'{INST_PATH}inst_offline_rating_3{os.sep}'
INST_CHOICE_TRUE = f'{INST_PATH}inst_choice_true{os.sep}'
INST_CHOICE_FALSE = f'{INST_PATH}inst_choice_false{os.sep}'
INST_LEARNING_CHECK = f'{INST_PATH}inst_learning_check{os.sep}'
INST_DEMAND_RATING = f'{INST_PATH}inst_demand_rating{os.sep}'
INST_END = f'{INST_PATH}inst_end{os.sep}'

### Stimuli Path ###
STIM_PATH = f'.{os.sep}stimuli{os.sep}'
STIM_2BACK_PRAC_PATH = f'{STIM_PATH}2_back_practice{os.sep}'
STIM_CALI_PATH = f'{STIM_PATH}2_back_calibration{os.sep}'
STIM_CUE_PRAC_PATH = f'{STIM_PATH}cue_practice{os.sep}'
STIM_CUE_LEARNING_PATH = f'{STIM_PATH}cue_learning{os.sep}'
STIM_CUE_CHOICE_PATH = f'{STIM_PATH}cue_choice{os.sep}'
STIM_CUE_OFFLINE_RATING_PATH = f'{STIM_PATH}cue_offline_rating{os.sep}'
STIM_CUE_LEARNING_CHECK_PATH = f'{STIM_PATH}cue_learning_check{os.sep}'

### TASK PARAMTERS ###
ISI_levels = list(range(1, 22))
ISI_values = [19, 50, 83, 120, 159, 202, 250, 303, 361, 426,
              500,
              583, 679, 788, 917, 1068, 1250, 1472, 1750, 2107, 2583]
ISIs = {str(i): ISI_values[-i] for i in ISI_levels}  # a dict of ISIs

trialNs_prac = range(1, 37)
trialNs_test = range(1, 51)

A_min = 0.75  # lowest performance level
A_max = 0.85  # highest performance level


# CUE-DEMAND MAPPING #
if PN % 2:  # if the PID is an odd number, use mapping A
    cue_map = 'A'
    cond_df = pd.read_csv(f".{os.sep}conditionsA.csv")
else:  # if the PID is an even number, use mapping B
    cue_map = 'B'
    cond_df = pd.read_csv(f".{os.sep}conditionsB.csv")

# Stimulus
FIXATION = visual.TextStim(win=WIN, text='+', height=.05, pos=[0, 0], color='white')
BLANK        = visual.TextStim(win=WIN, text='', height=.05, pos=[0, 0], color='white')
MentalDemand1 = f"How mentally demanding was \n\n the 1-Back letter memory task?"
Effort1 = f"How hard did you have to work in \n\n the 1-Back letter memory task?"
Frustration1 = f"How frustrated were you while performing \n\n the 1-Back letter memory task?"
MentalDemand2 = f"How mentally demanding was \n\n the 2-Back letter memory task?"
Effort2 = f"How hard did you have to work in \n\n the 2-Back letter memory task?"
Frustration2 = f"How frustrated were you while performing \n\n the 2-Back letter memory task?"
MentalDemand3 = f"How mentally demanding was \n\n the 3-Back letter memory task?"
Effort3 = f"How hard did you have to work in \n\n the 3-Back letter memory task?"
Frustration3 = f"How frustrated were you while performing \n\n the 3-Back letter memory task?"
DEMAND_RATING_QUES = {'MentalDemand1':MentalDemand1,
                      'Effort1': Effort1,
                      'Frustration1': Frustration1,
                      'MentalDemand2':MentalDemand2,
                      'Effort2': Effort2,
                      'Frustration2': Frustration2,
                      'MentalDemand3': MentalDemand3,
                      'Effort3': Effort3,
                      'Frustration3': Frustration3}

# Response
RESP_KEYS    = ['left', 'right'] # N-back response keys
RATING       = MS.getPos()


### TRIALS ###
TRIAL_NUM_CALI = 1  # 15 calibration trials (3 to debug)
TRIAL_NUM_PRAC_MAIN = 2  # 3 practice of rating
TRIAL_NUM_LEARNING = 1  # 50 test trials per block (1 to debug)
TRIAL_NUM_CHOICE_TRUE = 2  # 10 trials followed by 1 or 3-back (2 to debug)
TRIAL_NUM_CHOICE_FALSE = 2  # 50 trials always followed by 2-back (2 to debug)
TRIAL_NUM_OFFLINE_RATING = 2
TRIAL_NUM_LEARNING_CHECK = 2

### Timing ###
GLOBALCLOCK   = core.Clock()
RATING_TIMEOUT       = 3.000          # offline rating response window
CHOICE_TIMEOUT       = 3.000          # choice response window

FEEDBACK_DUR         = .500          # duration feedback is on screen

# BLOCK_TXT_DUR      = 1.000         # duration block info is on screen
TRIAL_INST_DUR       = 3.000          # duration instruction of trial demand

FIXA_CUE_DUR         = 1.500          # duration fixation prior to CUE
CUE_DUR              = 3.000          # duration cue is on screen
FIXA_SEQ_DUR         = 1.500          # duration fixation prior to CUE
FIXA_CHOICE_DUR      = 1.500          # duration fixation prior to CHOICE PROBE

FIXA_LETTER_DUR      =  .250          # duration fixation prior to letter (in each N-back Trial)


### ------------------------- ADMIN ------------------------- ###
if IF_SEE_COMPUTR_PLAY:
    AI_INSTRUCTION_TIME = 5.000  # 1.000