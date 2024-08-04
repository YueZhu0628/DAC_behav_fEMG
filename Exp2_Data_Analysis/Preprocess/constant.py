#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


# manually delete the blank rows and the 4th column in "DACFE_trigger.csv" file
triggers = pd.read_csv('DACFE_trigger.csv', header=0)
triggers["Binary"] = triggers["Binary"].astype(int) * 5
triggers["binary"] = triggers["Binary"].astype(str).str.zfill(8)
for i in range(triggers.shape[0]):
    triggers.loc[i,"binary"] = triggers.loc[i, "binary"][::-1]  # start, stop, stepsize = -1


# In[ ]:


# physio signal filter parameters
SAMPLE_RATE = 1_000


# In[ ]:


# trial numbers of each phase
TRIALN = {'Learning':50, 'TrueChoice':10, 'FalseChoice': 50, 'Offlines':8}


# In[ ]:





# In[ ]:


# reverse-score items
reverse_items = [
    # BAI 
    "BAI2_bis", "BAI22_bis",
    # NFC
    "NFC3", "NFC4", "NFC5", "NFC7", "NFC8", "NFC9", "NFC12", "NFC16", "NFC17",
    # BFI
    "BFI2_agr", "BFI6_ext", "BFI12_agr", "BFI18_con", "BFI21_ext",
    "BFI23_con", "BFI24_neu", "BFI27_agr", "BFI31_ext", "BFI34_neu",
    "BFI35_open", "BFI37_agr", "BFI41_open", "BFI43_con", 
    # UPPS
    "UPPS1_lps", "UPPS4_lps", "UPPS5_lpm", "UPPS7_lps", "UPPS12_lpm", "UPPS19_lpm"   
]


# In[ ]:


# scales of items
scales = {'BAI':4,'NFC':5,'BFI':5,'UPP':4}

