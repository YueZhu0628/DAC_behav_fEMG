from ...indicators.frequencydomain import *
from ...indicators.nonlinear import *
from ...indicators.peaks import *
from ...indicators.timedomain import *
# from ...sqi.sqi import *

def preset_phasic(delta, prefix="pha_"):
    mean = Mean()
    std = StDev()
    rng = Range()
    pks_max = PeaksMax(delta=delta)
    pks_min = PeaksMin(delta=delta)
    pks_mean = PeaksMean(delta=delta)
    n_peaks = PeaksNum(delta=delta)
    dur_mean = DurationMean(delta=delta, win_pre=2, win_post=2)
    """
    DurationMean function:

    Parameters
    ----------
    delta : float, >0
        Minimum amplitude of peaks to be selected
    win_pre : float, >0, default=1
        Interval before a detected peak where to search the start of the peak
    win_post : float, >0, default=1
        Interval after a detected peak where to search the end of the peak

    Returns
    -------
    av : float
        Average duration of detected peaks

    """
    slopes_mean = SlopeMean(delta=delta, win_pre=1.5, win_post=1.5)
    auc = AUC()

    t = [mean, std, rng, pks_max, pks_min, pks_mean, n_peaks, dur_mean, slopes_mean, auc]

    if prefix is not None:
        for i in t:
            i.set(name=prefix + i.__class__.__name__)

    return t


def preset_tonic(prefix="ton_"):
    mean = Mean()
    std = StDev()
    rng = Range()
    auc = AUC()

    t = [mean, std, rng, auc]

    if prefix is not None:
        for i in t:
            i.set(name=prefix + i.__class__.__name__)

    return t