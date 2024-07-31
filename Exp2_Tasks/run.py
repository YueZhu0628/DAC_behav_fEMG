# run.py file for DACFE.py
# coding=utf-8

# Use this script to run the experiment
# coding=utf-8

from src.constant import *   # task-specific global variables
from src import DACFE       # task-specific functions


### TRIGGER - START ###
this_trig = DF_TRIG[DF_TRIG.TriggerName=='expStart']['Code'].iloc[0]
sendTrigger(SER, this_trig)

## PHASE 0 - WELCOME ##
DACFE.show_instruction(INST_BEGIN, data=EXPDATA)


### ------------------------- 2-BACK PRACTICE PHASE ------------------------- ###
## PHASE 1 - PRACTICE 2-BACK PHASE - BEHAVIORAL ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'prac2BackStart']['Code'].iloc[0]  # Trigg Practice Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_PRAC_2, data=EXPDATA)
A = DACFE.trial_nBack(thisISI=ISIs['1'], nLevel=2, phase='practice', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0],
                    reminders=True, data=EXPDATA)  # return A
DACFE.check_A(A, A_min, A_max, ISI=ISIs['1'], nLevel=2, reminder=True)

toDo = DACFE.show_instruction(INST_TO_CALI, data=EXPDATA)
while toDo == 'left':
    DACFE.buffer(show="rePrac")

    A = DACFE.trial_nBack(thisISI=ISIs['1'], nLevel=2, phase='practice', block=0,
                        trialN=random.sample(trialNs_prac, 1)[0],
                        reminders=True, data=EXPDATA)  # return A
    DACFE.check_A(A, A_min, A_max, ISI=ISIs['1'], nLevel=2, reminder=True)

    toDo = DACFE.show_instruction(INST_TO_CALI, data=EXPDATA)
    if toDo == 'right':
        break


### ---------------------------- CALIBRATION PHASE ---------------------------- ###
## PHASE 2 - CALIBRATION PHASE - BEHAVIORAL ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'caliStart']['Code'].iloc[0]  # Trigg Practice Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_CALI, data=EXPDATA)

DACFE.buffer(show="start")
ISI_calibrated = DACFE.ISI_calibration(curr_ISI_level=10, data=EXPDATA)



### ------------------------- MAIN TASK PRACTICE PHASE ------------------------- ###
## PHASE 3 - 1-BACK PRACTICE PHASE ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'prac1BackStart']['Code'].iloc[0]  # Trigg Practice Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_PRAC_1, data=EXPDATA)
# ----- practice with reminders ----- #
A = DACFE.trial_nBack(thisISI=ISIs['5'], nLevel=1, phase='practice', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0],
                    reminders=True, data=EXPDATA)
DACFE.check_A(A, A_min, A_max, ISI=ISIs['5'], nLevel=1, reminder=True)
# practice again?
toDo = DACFE.show_instruction(INST_PRAC_1_NEXT, data=EXPDATA)
while toDo == 'left':
    DACFE.buffer(show="rePrac")
    A = DACFE.trial_nBack(thisISI=ISI_calibrated, nLevel=1, phase='practice', block=0,
                        trialN=random.sample(trialNs_prac, 1)[0],
                        reminders=True, data=EXPDATA)  # return A
    DACFE.check_A(A, A_min, A_max, ISI=ISI_calibrated, nLevel=1, reminder=True)
    toDo = DACFE.show_instruction(INST_PRAC_1_NEXT, data=EXPDATA)
    if toDo == 'right':
        break
# ----- practice without reminders ----- #
DACFE.buffer(show="start")
# 1-Back practice 1st trial
DACFE.trial_nBack(thisISI=ISI_calibrated, nLevel=1, phase='practice', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0],
                    reminders=False, data=EXPDATA)
DACFE.buffer(show="end_seq")
# 1-Back practice 2nd trial
A = DACFE.trial_nBack(thisISI=ISI_calibrated, nLevel=1, phase='practice', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0],
                    reminders=False, data=EXPDATA)  # return A
DACFE.check_A(A, A_min, A_max, ISI=ISI_calibrated, nLevel=1, reminder=False)

### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 4 - 3-BACK PRACTICE PHASE ##
DACFE.show_instruction(INST_PRAC_3, data=EXPDATA)
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'prac3BackStart']['Code'].iloc[0]  # Trigg Practice Phase
sendTrigger(SER, this_trig)

# ----- practice with reminders ----- #
A = DACFE.trial_nBack(thisISI=ISIs['8'], nLevel=3, phase='practice', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0],
                    reminders=True, data=EXPDATA)
DACFE.check_A(A, A_min, A_max, ISI=ISIs['8'], nLevel=3, reminder=True)
# practice again?
toDo = DACFE.show_instruction(INST_PRAC_3_NEXT, data=EXPDATA)
while toDo == 'left':
    DACFE.buffer(show="rePrac")
    A = DACFE.trial_nBack(thisISI=ISI_calibrated, nLevel=3, phase='practice', block=0,
                        trialN=random.sample(trialNs_prac, 1)[0],
                        reminders=True, data=EXPDATA)  # return A
    DACFE.check_A(A, A_min, A_max, ISI=ISI_calibrated, nLevel=3, reminder=True)
    toDo = DACFE.show_instruction(INST_PRAC_3_NEXT, data=EXPDATA)
    if toDo == 'right':
        break
# ----- practice without reminders ----- #
DACFE.buffer(show="start")
# 3-Back practice 1st trial
DACFE.trial_nBack(thisISI=ISI_calibrated, nLevel=3, phase='practice', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0],
                    reminders=False, data=EXPDATA)
DACFE.buffer(show="end_seq")
# 3-Back practice 2nd trial
A = DACFE.trial_nBack(thisISI=ISI_calibrated, nLevel=3, phase='practice', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0],
                    reminders=False, data=EXPDATA)  # return A
DACFE.check_A(A, A_min, A_max, ISI=ISI_calibrated, nLevel=3, reminder=False)

### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 5 - PRACTICE MAIN PHASE ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'pracMainStart']['Code'].iloc[0]  # Trigg Practice Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_PRAC_main, data=EXPDATA)

DACFE.main_block(phase='PRACTICE', testISI=ISI_calibrated, data=EXPDATA, block=0, run=RUN)
### ------ break ------ ###
DACFE.buffer(show="blank")
DACFE.show_instruction(INST_PRAC_end, data=EXPDATA) # Experimenter click the right button



### ------------------------- MAIN TASK PHASE ------------------------- ###

## PHASE 6 - OFFLINE-RATING (T0) ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'offlineT0Start']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_OFFLINE_RATING_T0, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
### ------ rating ----- ###
DACFE.offline_rating(data=EXPDATA, timepoint="T0")
### ------ break ------ ###
DACFE.buffer(show="blank")

# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'testStart']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)


## PHASE 7 - LEARNING PHASE ###
toDo = DACFE.show_instruction(INST_LEARNING, data=EXPDATA)
# practice again?
while toDo == 'left':
    DACFE.buffer(show="rePrac")
    # re-practice main task
    DACFE.show_instruction(INST_PRAC_main, data=EXPDATA, start_num=1)
    DACFE.buffer(show="start")
    DACFE.main_block(phase='PRACTICE', testISI=ISI_calibrated, data=EXPDATA, block=0, run=RUN)
    DACFE.buffer(show="blank")
    # until choose to start
    toDo = DACFE.show_instruction(INST_LEARNING, data=EXPDATA)
    if toDo == 'right':
        break

# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'learningStart']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

#  Block 1
DACFE.buffer(show="start_Test")
DACFE.main_block(phase='LEARNING', testISI=ISI_calibrated, data=EXPDATA, block=1, run=RUN)
# # only run Block 1
# # break for 2 minute
# DACFE.block_break_timer(120)
#
# #  Block 2
# DACFE.main_block(phase='LEARNING', testISI=ISI_calibrated, data=EXPDATA, block=2, run=RUN)

### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 8 - OFFLINE-RATING (T1) ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'offlineT1Start']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_OFFLINE_RATING_T1, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
### ------ rating ----- ###
DACFE.offline_rating(data=EXPDATA, timepoint="T1")
### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 9 - TRUE CHOICE PAHSE ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trueChoiceStart']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_CHOICE_TRUE, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
### ------ Demand choice ----- ###
DACFE.demand_choice(testISI=ISI_calibrated, phase="Choice", type="True", data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 10 - OFFLINE-RATING (T2) ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'offlineT2Start']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_OFFLINE_RATING_T2, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
### ------ rating ----- ###
DACFE.offline_rating(data=EXPDATA, timepoint="T2")
### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 11 - LEARNING-CHECK T1 ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'learningCheckT1Start']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_LEARNING_CHECK, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
DACFE.learning_check(data=EXPDATA, timepoint="T1")
### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 12 - FALSE CHOICE PAHSE ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'falseChoiceStart']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_CHOICE_FALSE, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
### ------ Demand choice ----- ###
DACFE.demand_choice(testISI=ISI_calibrated, phase="Choice", type="False", data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 13 - OFFLINE-RATING (T3) ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'offlineT3Start']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_OFFLINE_RATING_T3, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
### ------ rating ----- ###
DACFE.offline_rating(data=EXPDATA, timepoint="T3")
### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 13 - LEARNING-CHECK T2 ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'learningCheckT2Start']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_LEARNING_CHECK, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
DACFE.learning_check(data=EXPDATA, timepoint="T2")
### ------ break ------ ###
DACFE.buffer(show="blank")


## PHASE 14 - DEMAND-RATING PHASE ##
# send trigger
this_trig = DF_TRIG[DF_TRIG.TriggerName == 'demandRatingStart']['Code'].iloc[0]  # Trigg Phase
sendTrigger(SER, this_trig)

DACFE.show_instruction(INST_DEMAND_RATING, data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")
### ------ rating ------ ###
DACFE.demand_rating(data=EXPDATA)
### ------ break ------ ###
DACFE.buffer(show="blank")


### ------------------------- END ------------------------- ###

### TRIGGER - END ###
this_trig = DF_TRIG[DF_TRIG.TriggerName=='expEnd']['Code'].iloc[0]
sendTrigger(SER, this_trig)


## PHASE 15 - END - PSYCHOPY ##
DACFE.show_instruction(INST_END, data=EXPDATA)

### FINAL MESSAGE - TERMINAL ###
DACFE.terminal_final_msg()
WIN.flip()

### QUIT ###
core.quit()
EXPDATA.abort()
WIN.close()
