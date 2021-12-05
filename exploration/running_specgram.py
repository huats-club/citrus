from model.fft2dbm import fft2dbm
from model.SpectrogramPlotter import SpectrogramPlotter

if __name__ == "__main__":

    # read in fft data
    fft_data = []
    with open('C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data.txt') as f:
        fft_data = f.readlines()
        fft_data = [float(x.strip()) for x in fft_data]

    fft_data2 = [x+0.01 for x in fft_data]

    # create fft2dbm converter
    fft2dbm_conv = fft2dbm()

    # convert fft data into signal data
    latest_signal_data = fft2dbm_conv.convert(fft_data)
    latest_signal_data2 = fft2dbm_conv.convert(fft_data2)

    # waterfall plotter
    p = SpectrogramPlotter(740.3e6, 20e6)

    p.plot(latest_signal_data)

    for i in range(10):
        p.plot(latest_signal_data2)
