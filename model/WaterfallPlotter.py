import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


class WaterfallPlotter:
    def __init__(self, center_freq, bandwidth):

        # create plot space
        self.generate_figure()

        # generate (initial) timestamp marker
        ts_np = np.arange(20)

        # generate frequency bins
        freq_increment = bandwidth / 2048
        freq_bins = []
        start_freq = center_freq - bandwidth/2
        end_freq = center_freq + bandwidth/2
        while start_freq < end_freq:
            freq_bins.append(start_freq)
            start_freq += freq_increment
        freq_bins_np = np.asarray(freq_bins)

        # prepare 2d x,y data
        self.freq_bins_np_X, self.ts_np_Y = np.meshgrid(freq_bins_np, ts_np)

        # prepare z signal data store
        self.signal_np = np.zeros((0, 2048))

        # flag to indicate first data
        self.isFirst = True

        # incre
        self.incre = 1

    def generate_figure(self):

        plt.style.use("seaborn-dark")

        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey

        self.colors = [
            '#08F7FE',  # teal/cyan
            '#FE53BB',  # pink
            '#F5D300',  # yellow
            '#00ff41',  # matrix green
        ]

        self.fig = plt.figure(dpi=100)
        self.ax = self.fig.add_subplot(projection='3d')

        # set axis label
        self.ax.set_xlabel('freq_bins')
        self.ax.set_ylabel('timestamps')
        self.ax.set_zlabel('strength')

    def plot(self, latest_signal_data):

        # if is first time plot, populate all data with it
        if self.isFirst:

            num_ts = self.ts_np_Y.shape[0]

            for i in range(num_ts):
                self.signal_np = np.append(self.signal_np, [latest_signal_data], axis=0)
            self.signal_np = np.asarray(self.signal_np)

            self.isFirst = False

        # else pop oldest data and append latest data
        else:
            self.signal_np = np.delete(self.signal_np, 0, axis=0)
            self.signal_np = np.append(self.signal_np, [latest_signal_data], axis=0)

        # plot
        self.generate_figure()
        self.ax.set_zlim(-100, 10)
        self.surf = self.ax.plot_surface(
            self.freq_bins_np_X,
            self.ts_np_Y,
            self.signal_np,
            cmap=cm.get_cmap("jet"),
            antialiased=True,
            vmin=-90,
            vmax=-30
        )
        self.fig.colorbar(
            self.surf,
            location="left",
            orientation="vertical",
            ax=self.ax,
            shrink=0.4,
            aspect=30
        )
        # root = 'C:/Users/65844/Desktop/citrus/exploration/3dplot_data'
        # self.fig.savefig(f"{root}/3d_class_{self.incre}.png", bbox_inches='tight')
        # self.incre += 1
