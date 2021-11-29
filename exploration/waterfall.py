# https://stackoverflow.com/questions/56788798/python-spectrogram-in-3d-like-matlabs-spectrogram-function
# https://stackoverflow.com/questions/37711538/matplotlib-3d-axes-ticks-labels-and-latex

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from numpy.lib.function_base import interp  # colour map


def gen_data():
    '''
    Generate and save datas to txt file once
    '''

    # create timestamp data
    sample_rate = 11240
    sig_len_secs = 1
    timestamps_secs = np.arange(sample_rate*sig_len_secs) / sample_rate
    ts_np = np.asarray(timestamps_secs)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/ts_np", ts_np)

    # generate frequency bins data
    freq_increment = 20e6 / 2048
    freq_bins = []
    freq = 730.3e6
    end_freq = 730.3e6 + 20e6
    while freq < end_freq:
        freq_bins.append(freq)
        freq += freq_increment
    freq_bins_np = np.asarray(freq_bins)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/freq_bins_np", freq_bins_np)

    # read in fft data
    fft_data = []
    with open('C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data.txt') as f:
        fft_data = f.readlines()
        fft_data = [float(x.strip()) for x in fft_data]

    # process fft data to dbm
    signal_data = [20*math.log10(2*x / 1024) for x in fft_data]
    signal_data_np = np.asarray(signal_data)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/signal_data_np", signal_data_np)

    # prepare XY data for 3d plot
    freq_bins_np_X, ts_np_Y = np.meshgrid(freq_bins_np, ts_np)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/freq_bins_np_2d", freq_bins_np_X)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/ts_np_2d", ts_np_Y)

    # create z axis 2d data
    # format: f(x, y) -> z
    data_3dplot = []
    for i in range(ts_np.shape[0]):
        data_3dplot.append(signal_data)
    data_3dplot_np = np.asarray(data_3dplot)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data_3dplot_np", data_3dplot_np)

    # ----
    # gen 2d data
    data_2dplot = []
    for i in range(math.floor(ts_np.shape[0]/20)):
        data_2dplot.append(signal_data_np)
    data_2dplot_np = np.asarray(data_2dplot)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data_2dplot_np", data_2dplot_np)


if __name__ == "__main__":
    root = 'C:/Users/65844/Desktop/citrus/exploration/3dplot_data'
    ts_np_2d = np.load(f"{root}/ts_np_2d.npy")
    freq_bins_np_2d = np.load(f"{root}/freq_bins_np_2d.npy")
    data_3dplot_np = np.load(f"{root}/data_3dplot_np.npy")
    data_2dplot_np = np.load(f"{root}/data_2dplot_np.npy")
    # print(ts_np.shape)
    # print(freq_bins_np.shape)
    # print(dataset_np.shape)

    # 3d waterfall plot
    fig1 = plt.figure(num=1)
    ax1 = fig1.add_subplot(projection='3d')
    surf = ax1.plot_surface(
        freq_bins_np_2d,
        ts_np_2d,
        data_3dplot_np,
        cmap=cm.get_cmap("jet"),
        antialiased=True
    )
    fig1.colorbar(
        surf,
        location="bottom",
        orientation="horizontal",
        ax=ax1,
        shrink=0.4,
        aspect=30
    )
    ax1.set_xlabel('freq_bins')
    ax1.set_ylabel('timestamps')
    ax1.set_zlabel('spec')
    fig1.savefig(f"{root}/3d.png", bbox_inches='tight')
    # plt.show()

    # 2d waterfall plot
    fig2 = plt.figure(num=2)
    ax2 = fig2.add_subplot()
    waterfall2d = ax2.imshow(np.asarray(data_2dplot_np), cmap=cm.get_cmap("jet"), interpolation='bicubic')
    fig2.colorbar(
        waterfall2d,
        location="bottom",
        orientation="horizontal",
        ax=ax2,
        shrink=0.4,
        aspect=30
    )
    fig2.savefig(f"{root}/2d.png", bbox_inches='tight')
