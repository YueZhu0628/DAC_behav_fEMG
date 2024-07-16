# %preprocess physiological data files%
# compute values of zyg, cog, scr for each trigger in each trial
# combine physiological values to behavioral data file (one row per trial)
# coding=utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyphysio.pyphysio import signal, filters, segmenters, interactive
from pyphysio.pyphysio.specialized.eda import DriverEstim, PhasicEstim, preset_phasic

# load data
data = "007.txt"
col_names = ["zyg","scr","cor","trg1","trg2","trg3","trg4","trg5","trg6","trg7","trg8","na"]
df = pd.read_csv(data, sep='\t', names = col_names, index_col=False)


# separate phases
triggers = pd.read_csv("triggers.csv", sep='\t', names = ["triggerName","binary", "code"], index_col=False)


# parameters
samp_rate = 1_000
low_eda = 45
high_eda = 450

# create signal
zyg = signal.create_signal(df['zyg'], sampling_freq = samp_rate, name = 'zyg')
cor = signal.create_signal(df['cor'], sampling_freq = samp_rate, name = 'cor')
scr = signal.create_signal(df['scr'], sampling_freq = samp_rate, name = 'scr')
print(zyg)
label = signal.create_signal(df['marker'], sampling_freq = samp_rate, name = 'label')
# filtering and resampling
eda = filters.IIRFilter(fp = low_eda, fs = line_freq, btype = 'highpass', ftype='ellip')(eda)
# decouple SCR and SCL
driver = DriverEstim()(eda)
print(driver)
phasic = PhasicEstim(0.02)(driver)

# compute physiological indicators
segmenter = segmenters.LabelSegments(timeline=label, drop_mixed=False, drop_cut=False)
results = segmenters.fmap(segmenter, preset_phasic(delta=0.02), phasic)
# save data
df_res = results.to_dataframe()
df_res['duration'] = df_res['time_stop'] - df_res['time_start']
df_res.to_csv("results_EDA.csv",index = False)