import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import cm

warnings.simplefilter("ignore", UserWarning)


class SpectrogramPlotter:
    def __init__(self, center_freq, bandwidth):

        # create plot space
        self.generate_figure()

        # generate xticks
        xticks_exact = [center_freq - bandwidth/2, center_freq, center_freq + bandwidth/2]
        self.xticks_label = [x/1e6 for x in xticks_exact]

        # prepare z signal data store
        self.signal_datastore_np = np.zeros((0, 2048))

        # flag to indicate first data
        self.isFirst = True

        # incre
        self.incre = 1

    def generate_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

    def plot(self, latest_signal_data):

        # if is first time plot, populate all data with it
        if self.isFirst:

            for i in range(400):
                self.signal_datastore_np = np.append(self.signal_datastore_np, [latest_signal_data], axis=0)
            self.signal_datastore_np = np.asarray(self.signal_datastore_np)

            self.isFirst = False

        # else pop oldest data and append latest data
        else:

            curr_len = self.signal_datastore_np.shape[0]-1

            for i in range(12):
                self.signal_datastore_np = np.insert(self.signal_datastore_np, 0, [latest_signal_data], axis=0)
                self.signal_datastore_np = np.delete(self.signal_datastore_np, curr_len, axis=0)

        # plot
        self.generate_figure()
        self.waterfall2d = self.ax.imshow(self.signal_datastore_np, cmap=cm.get_cmap("jet"), interpolation='bicubic')
        self.fig.colorbar(
            self.waterfall2d,
            location="bottom",
            orientation="horizontal",
            ax=self.ax,
            shrink=0.4,
            aspect=30
        )
        self.ax.set_yticks([])
        self.ax.xaxis.set_major_locator(ticker.LinearLocator(numticks=3))
        self.ax.xaxis.set_major_formatter(ticker.FixedFormatter((self.xticks_label)))
        root = 'C:/Users/65844/Desktop/citrus/exploration/3dplot_data'
        self.fig.savefig(f"{root}/2d_class_{self.incre}.png", bbox_inches='tight')
        self.incre += 1