#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# loop through all participants


# In[1]:


# import defined functions
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from constant import *
import behavs
import physios
import ques


# In[ ]:





# In[14]:


def comb(df_behs, df_phys, df_ques, phase_names=['Individual','Learning','TrueChoice','FalseChoice','Offlines','LearningCheck','DemandRating']):
    df_combs = {}
    for phase in phase_names:
        if phase in ['Individual','LearningCheck', 'DemandRating']:
            df_b_p = df_behs[phase]
        else:
            df_b_p = df_behs[phase].merge(df_phys[phase], on="TrialN")
        df_comb = df_b_p.merge(df_ques, on="PID")
        df_combs[phase] = df_comb
    return df_combs


# In[3]:


def conc(df_combs, phase_names=['Learning','TrueChoice','FalseChoice','Offlines']):
    df_conc = pd.DataFrame()
    for phase in phase_names:
        df_conc = pd.concat(df_conc,df_combs[phase])
    return df_conc


# In[ ]:





# In[ ]:


# walk through all participants' data folders
# Define the root directory containing all participant folders
root_dir = 'E:\Dissertation\Methods\Exp2_Demand_Choice\Analysis\Exp2_data2'
PIDS = os.listdir(root_dir)

# Function to process each participant folder
def extrac_participant_files(participant_folder):
    # Construct the path to the "Data" subfolder
    data_folder = os.path.join(participant_folder, 'Data')
    Pfiles = {}
    pfiles = {}
    
    # Check if the "Data" subfolder exists
    if os.path.exists(data_folder):
        # Construct the expected file names
        pid = os.path.basename(participant_folder)
        print(pid)
        task_file = os.path.join(data_folder, pid + '_task.csv')
        survey_file = os.path.join(data_folder, pid + '_survey.csv')
        phy_file = os.path.join(data_folder, pid + '.txt')

        # Check if the files exist and print their paths
        for f in [task_file, survey_file, phy_file]:
            if os.path.exists(f):
                pass
            else:
                print(f"{f} miss!")
                
        pfiles['task'] = task_file
        pfiles['survey'] = survey_file
        pfiles['phy'] = phy_file

    return pfiles



# Walk through the root directory to find all participant folders
PFILES = {}
for participant_folder in os.listdir(root_dir):
    participant_path = os.path.join(root_dir, participant_folder)
    pid = os.path.basename(participant_folder)
    if os.path.isdir(participant_path):  # Ensure it's a directory
        pfiles = extrac_participant_files(participant_path)
        PFILES[pid] = pfiles


# In[5]:


# PFILES


# In[ ]:


PRES = {}
COMBRES = pd.DataFrame()
df_indi_all = pd.DataFrame()
df_learning_all = pd.DataFrame()
df_true_choice_all = pd.DataFrame()
df_false_choice_all = pd.DataFrame()
df_offlines_all = pd.DataFrame()
df_learnging_check_all = pd.DataFrame()
df_demandrating_all = pd.DataFrame()

for pid in PIDS:
    print('PID', pid)
    f_t = PFILES[pid]['task']
    df_behav_raw = behavs.load(f_t)
    print(1)
    df_behavs = behavs.phases(df_behav_raw)
    print(2)
    behavs.check_trial_n(df_behavs) != "Trial Numbers Correct!"
    print(3)

    f_p = PFILES[pid]['phy']
    df_phy_raw = physios.load(f_p,triggers)
    print(4)
    df_physios_raw = physios.phases(df_phy_raw)
    print(5)
    df_physios = physios.clean_phases(df_physios_raw)
    print(6)
    df_physios_res = physios.compute_phases(df_physios, TRIALN)
    df_physios_res_comb = {}
    for phase in ['Learning','TrueChoice','FalseChoice','Offlines']:
        df_physios_res_comb[phase] = df_physios_res[phase]['zyg'][['TrialN']]
        for channel in ['zyg','cor','scr']:
            df_physios_res1 = df_physios_res[phase][channel]
            df_physios_res_comb[phase] = df_physios_res_comb[phase].merge(df_physios_res1, on='TrialN')
    print(7)

    f_q = PFILES[pid]['survey']
    df_ques_raw = ques.load(f_q)
    print(8)
    df_ques_rev = ques.reverse_score(df_ques_raw, reverse_items, scales)
    print(9)
    df_ques_comp = ques.comp_scores(df_ques_rev)
    print(10)

    df_combs = comb(df_behavs, df_physios_res_comb, df_ques_comp)
    df_indi_all = pd.concat([df_indi_all, df_combs['Individual']])
    df_learning_all = pd.concat([df_learning_all, df_combs['Learning']])
    df_true_choice_all = pd.concat([df_true_choice_all, df_combs['TrueChoice']])
    df_false_choice_all = pd.concat([df_false_choice_all, df_combs['FalseChoice']])
    df_learnging_check_all = pd.concat([df_learnging_check_all, df_combs['LearningCheck']])
    df_demandrating_all = pd.concat([df_demandrating_all, df_combs['DemandRating']])
    
    PRES[pid] = df_combs


# # Individual information

# In[ ]:


# age, gender, mapping


# In[23]:


# ISI distribution]
# plt.plot(df_indi_all['NFC'].values)


# In[ ]:





# # Learning Phase

# In[ ]:


# Manipulatoin check (Task Performance)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[37]:


# standardize questionnaire scores after concatenate all participants df


# In[ ]:




