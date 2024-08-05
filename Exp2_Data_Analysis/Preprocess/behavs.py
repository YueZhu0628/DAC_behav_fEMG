#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# to prepross behavioral data file


# In[1]:


import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


# In[2]:


# load data
def load(datafile):
    col_names = ["PID","Age","Gender","Phase","Block", "TrialN", "NbackLevel", "ISI", 
                 # Calibration Info
                   "TrialCountCali", "CaliEnd_A_measure", "ISI_calibrated",
                 # Trial Info
                 "TrialIndex", "TrialNumber_total", "TrialNumber_valid",
                 # Trial Performance
                 "Trial_A_measure",
                 "Trial_ACC","Trial_RT",
                 "Letter_Resp", "Letter_RT", "Letter_Accuracy",
                 # Learning Phase 
                 "CueLearning", "CueMapping", "TrialDemandLearning",
                 # True & False choice
                 "CueLeft", "CueDemandLeft",
                 "CueRight", "CueDemandRight",
                 "PhaseType",
                 "Choice", "ChoiceRT",
                 "ChoiceDemand", "TaskDemand",
                 # Offline Rating T1, T2, T3
                 "OfflineRatingTimePoint",
                 "CueFigure", "TrialDemand",
                 "OfflineRating", "OfflineRatingRT",
                 # Learning check
                 "CueCheck", "CueDemandCheck", "CorrectAnswer",
                 "Answer", "AnswerDemand", "AnswerRT", "AnswerACC",
                 # Demand Rating
                 "DemandRatingQuesIndex", "QuesTLX", "DemandLevel", 
                 "DemandRating", "DemandRatingRT", 
                 # End
                 "END"]
    df = pd.read_csv(datafile, header=0, index_col=False, usecols=col_names)
    df.loc[df['Phase']=='OFFLINERATING',['TrialN']] = list(range(1,9))
    df['TrialN'] = df['TrialN'].fillna(-1).astype(int)
    return df


# In[32]:


# separate phases
def phases(df):
    def comb_trial_perf(df, phase, cols=["Trial_A_measure","Trial_ACC","Trial_RT"]):
        df_ct = df.copy()
        for col_t in cols:
            col = f'Task{col_t.replace("Trial","")}'
            df_ct[col] = df_ct[col_t].shift(1)
            df_ct_s = df_ct.loc[df_ct['Phase']==phase].sort_values('TrialN')      
        return df_ct_s
    df_indi = df[(df['Phase']=="PRACTICE") & (df['TrialN']==1)].copy()
    df_learnings = df[df['Phase'].isin(["LEARNING","Learning"])].copy()
    df_choices = df[df['Phase'].isin(["TrueCHOICE","FalseCHOICE","Choice"])]
    df_learning = comb_trial_perf(df_learnings,"LEARNING")
    df_choice_true = comb_trial_perf(df_choices,"TrueCHOICE")
    df_choice_false = comb_trial_perf(df_choices,"FalseCHOICE")
    
    df_offlines = df[df['Phase'] == "OFFLINERATING"].copy()
    df_learning_checks = df[df['Phase'] == "LEARNINGCHECK"].copy()
    df_demand_ratings = df[df['Phase'] == "DEMANDRATING"].copy().sort_values('DemandRatingQuesIndex')
    
    # return a dict of dfs
    df_behavs = {'Individual':df_indi,
                 'Learning':df_learning, 'TrueChoice':df_choice_true, 'FalseChoice':df_choice_false, 'Offlines':df_offlines,
                'LearningCheck':df_learning_checks, 'DemandRating':df_demand_ratings}
    stand_rt(df_behavs)
    stand_rating(df_behavs)
    return df_behavs


# In[4]:


# check for trial numbers
def check_trial_n(df_behavs):
    phase_names = ['Learning','TrueChoice','FalseChoice','Offlines']
    ns = []
    for phase in phase_names:
        pn = df_behavs[phase].shape[0]
        ns.append(pn)
    if ns == [50,10,50,8]:
        print("Trial Numbers Correct!")
    else:
        print("Error!", phase, ns)


# In[5]:


# check for whether learned the association
def check_learn(df_behavs):
    df = df_behavs['LearningCheck']
    pid = df['PID']
    df_check = df[['CueDemandCheck','CorrectAnswer','AnswerDemand','AnswerACC']]
    learn = df_check.loc[df_check['CorrectAnswer'].isin(["Left","Right"]),'AnswerACC'].mean(axis=0)
    delearn = df_check.loc[df_check['CorrectAnswer']=="Middle",'AnswerACC'].mean(axis=0)
    if (learn == 1) & (delearn == 1):
        pass
        # print("Learned well!")
    elif (learn == 1) & (delearn != 1):
        print(pid, "Learned well! Not De-Learned!")
    elif (learn != 1) & (delearn == 1):
        print(pid, "Not Learned! De-Learned well!")
    else:
        print(pid, "Fail both!")


# In[6]:


# standardize values
def stand_rt(df_behavs):
    for phase in ['Learning','TrueChoice','FalseChoice']:
        df = df_behavs[phase]
        df['Task_RT_z'] = stats.zscore(df['Task_RT'],nan_policy='omit')
        df['Task_RT_log'] = np.log(df['Task_RT'])
        df['Task_RT_log_z'] = stats.zscore(df['Task_RT_log'],nan_policy='omit')


# In[7]:


# standardize values
def stand_rating(df_behavs):
    for phase in ['Offlines','DemandRating']:
        df = df_behavs[phase]
        if phase == 'Offlines':
            col = 'OfflineRating'
        else:
            col = 'DemandRating'
        df[f'{col}_z'] = stats.zscore(df[col],nan_policy='omit')


# In[ ]:





# In[34]:


# datafile = "/Users/yolo/Documents/Coding/fEMG/DACFE_45/007/Data/007_task.csv"
# df = load(datafile)
# df_behavs = phases(df)
# df_behavs['FalseChoice']


# In[ ]:





# In[135]:


# df_behavs['Individual'][['PID','Age','Gender','ISI', 'CueMapping']]
# stand_rt(df_behavs)
# df_behavs['Learning'][['Trial_RT','Trial_RT_z','Trial_RT_log','Trial_RT_log_z']]
# stand_rating(df_behavs)
# df_behavs['Offlines']['OfflineRating_z']
# df_behavs['DemandRating'][['DemandLevel','DemandRating_z']]


# In[ ]:





# In[ ]:




