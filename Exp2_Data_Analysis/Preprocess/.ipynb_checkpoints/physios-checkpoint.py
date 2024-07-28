#!/usr/bin/env python
# coding: utf-8

# In[43]:


# %preprocess physiological data files%
# compute values of zyg, cog, scr for each trigger in each trial
# combine physiological values to behavioral data file (one row per trial)
# coding=utf-8

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from scipy.stats import zscore
from constant import *
from pyphysio.pyphysio import signal, filters, segmenters, interactive
from pyphysio.pyphysio.specialized.eda import DriverEstim, PhasicEstim, preset_phasic
from pyphysio.pyphysio.specialized.emg._presets import preset_femg


# In[2]:


# load data
def load(datafile, triggers):
    col_names = ["zyg","scr","cor","trg1","trg2","trg3","trg4","trg5","trg6","trg7","trg8","na"]
    data = pd.read_csv(datafile, sep='\t', names = col_names, index_col=False)
    data['line'] = np.array(list(np.linspace(0, data.shape[0]-1, data.shape[0])), int)
    data["binary"] = data.trg1.astype(str) + data.trg2.astype(str) + data.trg3.astype(str) + \
    data.trg4.astype(str) + data.trg5.astype(str) + data.trg6.astype(str) + \
    data.trg7.astype(str) + data.trg8.astype(str)
    df = data.merge(triggers, on="binary").drop(["Binary"], axis=1).sort_values(by='line')
    return df


# In[3]:


# separate phases
def phases(df):
    df['Phase'] = ''
    line_idxs = {}
    phase_names = list(triggers['TriggerName'][triggers['TriggerName'].str.endswith(("Start", "End"))])
    for phase in phase_names:
        line_i = np.where(df['TriggerName']== phase)[0][0]
        line_n = df.line.iloc[line_i]
        line_idxs[phase]=line_n
    # Practice Start
    df.loc[df.line.isin(range(line_idxs['prac2BackStart'],line_idxs['caliStart'])),'Phase'] = "Practice2Back"
    df.loc[df.line.isin(range(line_idxs['caliStart'],line_idxs['prac1BackStart'])),'Phase'] = "Calibration"
    df.loc[df.line.isin(range(line_idxs['prac1BackStart'],line_idxs['prac3BackStart'])),'Phase'] = "Practice1Back"
    df.loc[df.line.isin(range(line_idxs['prac3BackStart'],line_idxs['testStart'])),'Phase'] = "Practice3Back"
    # Test Start
    df.loc[df.line.isin(range(line_idxs['offlineT0Start'],line_idxs['learningStart'])),'Phase'] = "OfflineRatingT0"
    df.loc[df.line.isin(range(line_idxs['learningStart'],line_idxs['offlineT1Start'])),'Phase'] = "Learning"
    df.loc[df.line.isin(range(line_idxs['offlineT1Start'],line_idxs['trueChoiceStart'])),'Phase'] = "OfflineRatingT1"
    df.loc[df.line.isin(range(line_idxs['trueChoiceStart'],line_idxs['offlineT2Start'])),'Phase'] = "TrueChoice"
    
    df.loc[df.line.isin(range(line_idxs['offlineT2Start'],line_idxs['learningCheckT1Start'])),'Phase'] = "OfflineRatingT2"
    df.loc[df.line.isin(range(line_idxs['learningCheckT1Start'],line_idxs['falseChoiceStart'])),'Phase'] = "LearningCheckT1"
    df.loc[df.line.isin(range(line_idxs['falseChoiceStart'],line_idxs['offlineT3Start'])),'Phase'] = "FalseChoice"
    df.loc[df.line.isin(range(line_idxs['offlineT3Start'],line_idxs['learningCheckT2Start'])),'Phase'] = "OfflineRatingT3"
    df.loc[df.line.isin(range(line_idxs['learningCheckT2Start'],line_idxs['demandRatingStart'])),'Phase'] = "LearningCheckT2"
    # Demand Manipulation Check
    df.loc[df.line.isin(range(line_idxs['demandRatingStart'],line_idxs['expEnd'])),'Phase'] = "DemandRating"
    # separate phases
    df_learning = df[df['Phase'] == "Learning"].copy().sort_values('line')
    df_true_choice = df[df['Phase'] == "TrueChoice"].copy().sort_values('line')
    df_false_choice = df[df['Phase'] == "FalseChoice"].copy().sort_values('line')
    df_offlines = df[df['Phase'].str.startswith("OfflineRating")].copy().sort_values('line')
    df_learning_checks = df[df['Phase'].str.startswith("LearningCheck")].copy().sort_values('line')
    df_demand_ratings = df[df['Phase'] == "DemandRating"].copy().sort_values('line')
    # combine into a dict
    df_physios_raw = {'Learning':df_learning, 'TrueChoice':df_true_choice, 'FalseChoice':df_false_choice, 'Offlines':df_offlines,
                     'LearningCheck':df_learning_checks, 'DemandRating':df_demand_ratings}
    return df_physios_raw


# In[4]:


# add trial number
def add_trial_n(df):
    trial_n = []
    trial_count = 0            
    for i in range(df.shape[0]):
        if df['TriggerName'].iloc[i] == "trialStart":
            if df['TriggerName'].iloc[i+1] != "trialStart":
                trial_count += 1
        if df['TriggerName'].iloc[i] == "trialEnd":
            pass
        trial_n.append(trial_count)
    df_trialed = df.copy()
    df_trialed['Trial_N'] = trial_n
    return df_trialed


# In[5]:


def ex_timeout(df):
    rep = 0
    df_in = df.copy()
    while sum(df['TriggerName']=="respChoiceTimeout"):
        rep += 1
        trial_ex = set(df[df['TriggerName']=="respChoiceTimeout"].Trial_N)
        trial_in = set(df.Trial_N) - trial_ex
        df_in = df[df['Trial_N'].isin(trial_in)].copy()
        if rep == 3:
            break
    return df_in


# In[6]:


def clean_phases(dfs, phase_names=['Learning','TrueChoice','FalseChoice','Offlines']):
    df_physios = {}
    for phase in phase_names:
        df_p = dfs[phase]
        df_trialed = add_trial_n(df_p)
        df_in = ex_timeout(df_trialed)
        df_physios[phase] = df_in
    return df_physios


# In[101]:


def ex_outliers_iqr(df, event, channel, gpb='label'):
    if channel in ['zyg','cor']:
        col = f'{event}_{channel}_IIRFilter_NotchFilter_femg_mean'
    elif channel == 'scr':
        col = f'{event}_{channel}_IIRFilter_DriverEstim_PhasicEstim_pha_DurationMean'
    iqrs = df.groupby(gpb)[col].quantile([0.05, 0.95]).unstack(level=1)
    low_outs = iqrs.loc[df[gpb],0.05] > df[col].values
    high_outs = iqrs.loc[df[gpb],0.95] < df[col].values
    ts = set(df['trialn'].values)
    t_outs = set(df.loc[(low_outs | high_outs).values]['trialn'].values)
    t_ins = ts - t_outs
    df_clean = df[df['trialn'].isin(t_ins)]
    return df_clean


# In[133]:


def diff_values(df_c, trialn, event, channel):
    trials = range(1, trialn+1)
    diffs_dict = {'trials':trials}
    trials_in = set(df_c['trialn'].values)
    values = []
    if channel in ['zyg', 'cor']:
        col = f'{event}_{channel}_IIRFilter_NotchFilter_femg_mean'
    elif channel == 'scr':
        col = f'{event}_{channel}_IIRFilter_DriverEstim_PhasicEstim_pha_DurationMean'
    for i in trials:
        if i in trials_in:
            df = df_c.loc[df_c['trialn']==i,['label',col]]
            idx = list(df.columns).index(col)
            df.iloc[0, idx]
            fixa = df.iloc[0, idx]
            target = df.iloc[1, idx]
            diff = target - fixa
        else:
            diff = np.nan
        values.append(diff)
        zvalues = zscore(values, nan_policy='omit')
    diffs_dict[f'{event}_{channel}_values'] = values
    diffs_dict[f'{event}_{channel}_zvalues'] = zvalues
    df_diffs = pd.DataFrame(diffs_dict)
    return df_diffs


# In[134]:


def signal_compute(df_p, samp_rate, event, trialn, channels=['zyg','cor','scr']):
    if event == "cue_i":
        events = ['fixaCue', 'cueEasy', 'cueHard']
    elif event == "cue_e_true":
        events = ['fixaSeq', 'seqStart_N1', 'seqStart_N3']
    elif event == "cue_e_false":
        events = ['fixaSeq', 'seqStart_N2']
    df = df_p[df_p['TriggerName'].isin(events)]
    label = signal.create_signal(df['Code'], sampling_freq = samp_rate, name = 'label')
    df_results = {}
    # filters
    for channel in channels:
        # print(channel)
        if channel in ['zyg', 'cor']:
            femg = signal.create_signal(df[channel], sampling_freq = samp_rate, name = f'{event}_{channel}')
            bandpass = filters.IIRFilter(fp=45, fs=450, btype='bandpass', ftype='butter')(femg)
            rectify = bandpass.copy()
            rectify[f'{event}_{channel}_IIRFilter'] = abs(bandpass[f'{event}_{channel}_IIRFilter'])
            notch = filters.NotchFilter(f=50)(rectify)
            norm = filters.Normalize(notch)
            df_filtered = notch
            # compute values
            segmenter = segmenters.LabelSegments(timeline=label, drop_mixed=False, drop_cut=False)
            results = segmenters.fmap(segmenter, preset_femg(), df_filtered)
        elif channel in ['scr']:
            eda = signal.create_signal(df[channel], sampling_freq = samp_rate, name = f'{event}_{channel}')
            eda /= 10
            bandpass = filters.IIRFilter(fp=0.8, fs=1.1, btype='bandpass', ftype='ellip')(eda)
            driver = DriverEstim()(bandpass)
            phasic = PhasicEstim(0.02)(driver)
            norm = filters.Normalize(phasic)
            df_filtered = phasic
            # compute values
            segmenter = segmenters.LabelSegments(timeline=label, drop_mixed=False, drop_cut=False)
            results = segmenters.fmap(segmenter, preset_phasic(delta=0.02), df_filtered)
        else:
            print('wrong channel!')
        df_res = results.to_dataframe()
        tn = sorted(list(range(1, int(df_res.shape[0]/2)+1))*2)
        df_res['trialn'] = tn
        df_res_clean = ex_outliers_iqr(df_res, event, channel)
        df_res_diff = diff_values(df_res_clean, trialn, event, channel)
        df_res_diff = df_res_diff.rename(columns={'trials':'TrialN'})
        df_results[channel] = df_res_diff
    
    return df_results


# In[135]:


# def diff_values(dfs, trials, channels=['zyg','cor','scr']):
#     values = []
#     trials_in = set(df['trialn'].values)
#     for i in trials:
#         if i in trials_in:
#             df = df_res_clean.loc[df_res_clean['trialn']==i,['label',f'{channel}_IIRFilter_NotchFilter_femg_mean']]
#             idx = list(df.columns).index(f'{channel}_IIRFilter_NotchFilter_femg_mean')
#             df.iloc[0, idx]
#             fixa = df.iloc[0, idx]
#             target = df.iloc[1, idx]
#             diff = target - fixa
#         else:
#             diff = np.nan
#         values.append(diff)
#         zvalues = zscore(values, nan_policy='omit')
#     diffs = pd.DataFrame({'trials':trials, f'{channel}_values':values, f'{channel}_zvalues':zvalues})
#     return diffs


# In[136]:


def compute_phases(dfs, trialns, phase_names=['Learning','TrueChoice','FalseChoice','Offlines'], samp_rate=1_000):
    df_results = {}
    for phase in phase_names:
        df = dfs[phase]
        trialn = trialns[phase]
        if phase == 'Learning':
            df_result = {}
            df_result_cue_i = signal_compute(df, samp_rate, "cue_i", trialn)
            df_result_cue_e = signal_compute(df, samp_rate, "cue_e_true", trialn)
            for channel in ['zyg','cor','scr']:
                df_result[channel] = df_result_cue_i[channel].merge(df_result_cue_e[channel], on='TrialN')
        elif phase == "TrueChoice":
            df_result = signal_compute(df, samp_rate, "cue_e_true", trialn)
        elif phase == "TrueChoice":
            df_result = signal_compute(df, samp_rate, "cue_e_false", trialn)
        elif phase == "Offlines":
            df_result = signal_compute(df, samp_rate, "cue_i", trialn)
        
        df_results[f'{phase}'] = df_result
    return df_results


# In[150]:


# f_p = "E:\Dissertation\Methods\Exp2_Demand_Choice\Analysis\Exp2_data2\\007\Data\\007.txt"
# df_phy_raw = load(f_p,triggers)
# df_physios_raw = phases(df_phy_raw)
# df_physios = clean_phases(df_physios_raw)
# df_physios_res = compute_phases(df_physios, TRIALN)
# df_physios_res_comb = {}
# for phase in ['Learning','TrueChoice','FalseChoice','Offlines']:
#     df_physios_res_comb[phase] = df_physios_res[phase]['zyg'][['trials']]
#     for channel in ['zyg','cor','scr']:
#         df_physios_res1 = df_physios_res[phase][channel]
#         df_physios_res_comb[phase] = df_physios_res_comb[phase].merge(df_physios_res1, on='trials')


# In[153]:


# df_physios_res_comb['Learning']


# In[108]:


# df_p = df_physios['Learning']
# events = ['fixaSeq', 'seqStart_N1', 'seqStart_N3']
# samp_rate = 1_000
# df = df_p[df_p['TriggerName'].isin(events)]
# label = signal.create_signal(df['Code'], sampling_freq = samp_rate, name = 'label')
# eda = signal.create_signal(df_physios['Learning']['scr'], sampling_freq = 1_000, name = 'scr')
# eda /= 10
# bandpass = filters.IIRFilter(fp=0.8, fs=1.1, btype='bandpass', ftype='ellip')(eda)
# driver = DriverEstim()(bandpass)
# phasic = PhasicEstim(0.02)(driver)
# # norm = filters.Normalize(phasic)
# df_filtered = phasic
# # # compute values
# segmenter = segmenters.LabelSegments(timeline=label, drop_mixed=False, drop_cut=False)
# results = segmenters.fmap(segmenter, preset_phasic(delta=0.02), df_filtered)


# In[15]:


# df_physios['Learning'][df_physios['Learning']['TriggerName'].isin(['fixaSeq', 'seqStart_N1', 'seqStart_N3'])].groupby('Code').mean()


# In[ ]:





# In[ ]:




