#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# to preprocess questionnaires data file


# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[8]:





# In[12]:





# In[55]:


# load data
# datafile = "E:\Dissertation\Methods\Exp2_Demand_Choice\Analysis\Exp2_data2\\007\Data\\007_survey.csv"
def load(datafile):
    col_names = ["PID",
                 # BAI
                 "BAI1_filler","BAI2_bis","BAI3_bas_d","BAI4_bas_rr","BAI5_bas_fs","BAI6_filler","BAI7_bas_rr","BAI8_bis",
                 "BAI9_bas_d","BAI10_bas_fs","BAI11_filler","BAI12_bas_d","BAI13_bis","BAI14_bas_rr","BAI15_bas_fs","BAI16_bis",
                 "BAI17_filler","BAI18_bas_rr","BAI19_bis","BAI20_bas_fs","BAI21_bas_d","BAI22_bis","BAI23_bas_rr","BAI24_bis",
                 # NFC
                 "NFC1","NFC2","NFC3","NFC4","NFC5","NFC6",
                 "NFC7","NFC8","NFC9","NFC10","NFC11","NFC12",
                 "NFC13","NFC14","NFC15","NFC16","NFC17","NFC18",
                 # BFI
                 "BFI1_ext","BFI2_agr","BFI3_con","BFI4_neu","BFI5_open","BFI6_ext","BFI7_agr","BFI8_con","BFI9_neu","BFI10_open","BFI11_ext",
                 "BFI12_agr","BFI13_con","BFI14_neu","BFI15_open","BFI16_ext","BFI17_agr","BFI18_con","BFI19_neu","BFI20_open","BFI21_ext","BFI22_agr",
                 "BFI23_con","BFI24_neu","BFI25_open","BFI26_ext","BFI27_agr","BFI28_con","BFI29_neu","BFI30_bas_rr","BFI31_ext","BFI32_agr","BFI33_con",
                 "BFI34_neu","BFI35_open","BFI36_ext","BFI37_agr","BFI38_con","BFI39_neu","BFI40_open","BFI41_open","BFI42_agr","BFI43_con","BFI44_open",
                 # UPPS
                 "UPPS1_lps","UPPS2_lpm","UPPS3_pu","UPPS4_lps","UPPS5_lpm",
                 "UPPS6_nu","UPPS7_lps","UPPS8_nu","UPPS9_ss","UPPS10_pu",
                 "UPPS11_lps","UPPS12_lpm","UPPS13_nu","UPPS14_ss","UPPS15_nu",
                 "UPPS16_ss","UPPS17_pu","UPPS18_ss","UPPS19_lpm","UPPS20_pu"]
    df = pd.read_csv(datafile, header=0, index_col=False, usecols=col_names, nrows=1)
    df.rename(columns={'BFI30_bas_rr':'BFI30_open'}) # a typo in questionnaire script
    return df


# In[15]:


def reverse_score(df, items, scales):
    df_ques = df.copy()
    for item in items:
        v = item[0:3]
        df_ques[item] = scales[v] - (df[item]+1)
    return df_ques


# In[79]:


# sum, ave, standardize scores
# df_ques = reverse_score(df, reverse_items, scales)


# In[76]:


def comp_scores(df):
    df_comp = pd.DataFrame()
    items = df.columns.values.tolist()
    # BAI
    items_BAI_bis = []
    items_BAI_bas_d = []
    items_BAI_bas_rr = []
    items_BAI_bas_fs = []
    # NFC
    items_NFC = []
    # BFI
    items_BFI_ext = []
    items_BFI_agr = []
    items_BFI_con = []
    items_BFI_neu = []
    items_BFI_open = []

    #UPPS
    items_UPPS_lps = []
    items_UPPS_lpm = []
    items_UPPS_pu = []
    items_UPPS_ss = []
    
    for item in items:
        if 'BAI' in item:
            if 'bis' in item:
                items_BAI_bis.append(item)
            elif 'bas_d' in item:
                items_BAI_bas_d.append(item)
            elif 'bas_rr' in item:
                items_BAI_bas_rr.append(item)
            elif 'bas_fs' in item:
                items_BAI_bas_fs.append(item)

        # NFC
        elif 'NFC' in item:
            items_NFC.append(item)

        # BFI
        elif 'BFI' in item:
            if 'ext' in item:
                items_BFI_ext.append(item)
            elif 'agr' in item:
                items_BFI_agr.append(item)
            elif 'con' in item:
                items_BFI_con.append(item)
            elif 'neu' in item:
                items_BFI_neu.append(item)
            elif 'open' in item:
                items_BFI_open.append(item)

        # UPPS
        elif 'UPPS' in item:
            if 'lps' in item:
                items_UPPS_lps.append(item)
            elif 'lpm' in item:
                items_UPPS_lpm.append(item)
            elif 'pu' in item:
                items_UPPS_pu.append(item)
            elif 'ss' in item:
                items_UPPS_ss.append(item)
    
    df_comp['PID'] = df['PID']      
    
    df_comp['BAI_bis'] = df[items_BAI_bis].mean(axis=1)
    df_comp['BAI_bas_d'] = df[items_BAI_bas_d].mean(axis=1)
    df_comp['BAI_bas_rr'] = df[items_BAI_bas_rr].mean(axis=1)
    df_comp['BAI_bas_fs'] = df[items_BAI_bas_fs].mean(axis=1)
    
    df_comp['NFC'] = df[items_NFC].mean(axis=1)
    
    df_comp['BFI_ext'] = df[items_BFI_ext].mean(axis=1)
    df_comp['BFI_agr'] = df[items_BFI_agr].mean(axis=1)
    df_comp['BFI_con'] = df[items_BFI_con].mean(axis=1)
    df_comp['BFI_neu'] = df[items_BFI_neu].mean(axis=1)
    df_comp['BFI_open'] = df[items_BFI_open].mean(axis=1)
    
    df_comp['UPPS_lps'] = df[items_UPPS_lps].mean(axis=1)
    df_comp['UPPS_lpm'] = df[items_UPPS_lpm].mean(axis=1)
    df_comp['UPPS_pu'] = df[items_UPPS_pu].mean(axis=1)
    df_comp['UPPS_ss'] = df[items_UPPS_ss].mean(axis=1)

    return df_comp


# In[ ]:




