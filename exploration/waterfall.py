# https://stackoverflow.com/questions/56788798/python-spectrogram-in-3d-like-matlabs-spectrogram-function

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm  # colour map
from scipy import signal  # spectrogram function

# basic config
sample_rate = 11240.  #
sig_len_secs = 10
frequency = 2000.

# generate the signal
timestamps_secs = np.arange(sample_rate*sig_len_secs) / sample_rate
mysignal = np.sin(2.0 * np.pi * frequency * timestamps_secs)

# extract the spectrum
freq_bins, timestamps, spec = signal.spectrogram(mysignal, sample_rate)

# 3d plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(freq_bins[:, None], timestamps[None, :], 10.0*np.log10(spec), cmap=cm.get_cmap("coolwarm"))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
