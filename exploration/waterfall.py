# https://stackoverflow.com/questions/56788798/python-spectrogram-in-3d-like-matlabs-spectrogram-function
# https://stackoverflow.com/questions/37711538/matplotlib-3d-axes-ticks-labels-and-latex

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm  # colour map


def gen_data():
    '''
    Generate and save datas to txt file once
    '''

    # create timestamp data
    sample_rate = 11240
    sig_len_secs = 1
    timestamps_secs = np.arange(sample_rate*sig_len_secs) / sample_rate
    ts_np = np.asarray(timestamps_secs)

    # generate frequency bins data
    freq_increment = 20e6 / 2048
    freq_bins = []
    freq = 730.3e6
    end_freq = 730.3e6 + 20e6
    while freq < end_freq:
        freq_bins.append(freq)
        freq += freq_increment
    freq_bins_np = np.asarray(freq_bins)

    # read in fft data
    fft_data = []
    with open('C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data.txt') as f:
        fft_data = f.readlines()
        fft_data = [float(x.strip()) for x in fft_data]

    # process fft data to dbm
    signal_data = [20*math.log10(2*x / 1024) for x in fft_data]
    freq_bins_np_X, ts_np_Y = np.meshgrid(freq_bins_np, ts_np)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/freq_bins_np", freq_bins_np_X)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/ts_np", ts_np_Y)

    # create z axis 2d data
    # format: f(x, y) -> z
    dataset = []
    for i in range(ts_np.shape[0]):
        dataset.append(signal_data)
    dataset_np = np.asarray(dataset)
    np.save("C:/Users/65844/Desktop/citrus/exploration/3dplot_data/dataset_np", dataset_np)


if __name__ == "__main__":
    root = 'C:/Users/65844/Desktop/citrus/exploration/3dplot_data/'
    ts_np = np.load(f"{root}/ts_np.npy")
    freq_bins_np = np.load(f"{root}/freq_bins_np.npy")
    dataset_np = np.load(f"{root}/dataset_np.npy")
    print(ts_np.shape)
    print(freq_bins_np.shape)
    print(dataset_np.shape)

    # 3d plot
    fig = plt.figure(1)
    ax = fig.add_subplot(projection='3d')
    surf = ax.plot_surface(
        freq_bins_np,
        ts_np,
        dataset_np,
        cmap=cm.get_cmap("rainbow"),
        antialiased=True
    )
    fig.colorbar(
        surf,
        location="bottom",
        orientation="horizontal",
        ax=ax,
        shrink=0.4,
        aspect=30
    )
    ax.set_xlabel('freq_bins')
    ax.set_ylabel('timestamps')
    ax.set_zlabel('spec')
    fig.savefig(f"{root}/3d.png")
    plt.show()
