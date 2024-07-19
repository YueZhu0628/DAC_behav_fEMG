from ...indicators.frequencydomain import *
from ...indicators.nonlinear import *
from ...indicators.peaks import *
from ...indicators.timedomain import *
# from ...sqi.sqi import *
# I add two dots in front of the module in  "from" lines

def preset_emg(prefix='emg_', method = 'welch'):
    mx = Max(name='maximum')
    mn = Min(name='minimum')
    mean = Mean(name='mean')
    rng = Range(name='range')
    sd = StDev(name='sd')
    auc = AUC(name='auc')
    en4_40 = PowerInBand(freq_min=4, freq_max=40, method=method, name="en_4_40")
    
    t = [mx, mn, mean, rng, sd, auc, en4_40]

    if prefix is not None:
        for i in t:
            i.set(name=prefix + i.get("name"))

    return t

# define the function for my fEMG study (Boxtel, 2010)
def preset_femg(prefix='femg_', method='welch'):
    mx = Max(name='maximum')
    mn = Min(name='minimum')
    mean = Mean(name='mean')
    rng = Range(name='range')
    sd = StDev(name='sd')
    auc = AUC(name='auc')
    en40_450 = PowerInBand(freq_min=40, freq_max=450, method=method, name="en_40_450")

    t = [mx, mn, mean, rng, sd, auc, en40_450]

    if prefix is not None:
        for i in t:
            i.set(name=prefix + i.get("name"))

    return t