# https://stackoverflow.com/questions/56788798/python-spectrogram-in-3d-like-matlabs-spectrogram-function
# https://stackoverflow.com/questions/37711538/matplotlib-3d-axes-ticks-labels-and-latex

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm  # colour map
from scipy import signal  # spectrogram function
from scipy.interpolate import griddata


def sample_plot():
    # basic config
    sample_rate = 11240.  #
    sig_len_secs = 10
    frequency = 2000.

    # generate the signal
    timestamps_secs = np.arange(sample_rate*sig_len_secs) / sample_rate
    mysignal = np.sin(2.0 * np.pi * frequency * timestamps_secs)

    # extract the spectrum
    freq_bins, timestamps, spec = signal.spectrogram(mysignal, sample_rate)
    print(type(freq_bins))
    print(type(timestamps))
    print(type(spec))
    print(freq_bins.ndim)
    print(timestamps.ndim)
    print(spec.ndim)

    # 3d plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(freq_bins[:, None], timestamps[None, :], 10.0*np.log10(spec), cmap=cm.get_cmap("coolwarm"))
    ax.set_xlabel('freq_bins')
    ax.set_ylabel('timestamps')
    ax.set_zlabel('spec')
    plt.show()


if __name__ == "__main__":
    # create timestamp data
    sample_rate = 11240
    sig_len_secs = 1
    timestamps_secs = np.arange(sample_rate*sig_len_secs) / sample_rate
    ts_np = np.asarray(timestamps_secs)
    print(ts_np.shape)

    # generate frequency bins data
    freq_increment = 20e6 / 2048
    freq_bins = []
    freq = 730.3e6
    end_freq = 730.3e6 + 20e6
    while freq < end_freq:
        freq_bins.append(freq)
        freq += freq_increment
    freq_bins_np = np.asarray(freq_bins)
    print(freq_bins_np.shape)

    # read in fft data
    fft_data = []
    with open('C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data.txt') as f:
        fft_data = f.readlines()
        fft_data = [float(x.strip()) for x in fft_data]

    # process fft data to dbm
    signal_data = [20*math.log10(2*x / 1024) for x in fft_data]

    X, Y = np.meshgrid(freq_bins_np, ts_np)

    # create z axis 2d data
    # format: f(x, y) -> z
    dataset = []
    for i in range(ts_np.shape[0]):
        dataset.append(signal_data)
    dataset_np = np.asarray(dataset)
    print(dataset_np.shape)

    # 3d plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    surf = ax.plot_surface(
        X,
        Y,
        dataset_np,
        cmap=cm.get_cmap("coolwarm"),
        antialiased=True
    )
    fig.colorbar(surf, shrink=0.5)
    ax.set_xlabel('freq_bins')
    ax.set_ylabel('timestamps')
    ax.set_zlabel('spec')
    plt.show()
