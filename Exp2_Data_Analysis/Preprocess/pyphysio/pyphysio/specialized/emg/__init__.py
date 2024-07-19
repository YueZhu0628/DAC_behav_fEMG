import numpy as _np
import scipy.optimize as _opt
from ... import create_signal
from ..._base_algorithm import _Algorithm
# from ...signal import create_signal
from ...filters import DeConvolutionalFilter as _DeConvolutionalFilter, \
    ConvolutionalFilter as _ConvolutionalFilter, IIRFilter as _IIRFilter
from ...utils import PeakDetection as _PeakDetection, PeakSelection as _PeakSelection

from ._presets import *

