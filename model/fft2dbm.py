import math

import numpy as np


class fft2dbm:
    def __init__(self):
        pass

    def convert(self, fft_data):
        signal_data = [20*math.log10(2*x / 1024) for x in fft_data]
        return signal_data
