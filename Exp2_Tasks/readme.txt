'DARDCfEMG' PsychoPy Program written in Python
Author: Yue Zhu  
Date: Feb.18, 2024

----------------------------------------------
DARDC is short for Demand-Affective-Rating-Demand-Choice. 
DARDC is a fEMG  experiment to test the influence of cognitive demand on effort decision-making. Offline affective evaluatoin is also measured.
-----------------------------------------------------------------------------------------------------------

This python project is comprised of three .py files, the instructions folder and the stimuli folder.

constant.py: set up constant parameters.
DARDCfEMG.py: define functions and procedures to be used in 'run.py'.
run.py: run this file when conducting experiment.

instructions folder: instruction slides (.pptx file) and images (.png files).
stimuli folder: four images used as cues. Two for practice and two for test phases (.png files).
letter stimuli for N-Back tasks are save as variables in 'letter_stimuli.py'.

Notes:
(1) There are 4 Runs in each 'n_back_trials' folders. They were used in Vogel (2020)'s research in case the participants have to re-run the program. The default run is set = 1. The experimenter should change the number (2, 3, or 4) when re-running the program.
(2) Trial sequence in Practice is randomly sampled fron "conditionsA/B.csv" file. 