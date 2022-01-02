import math
import time

import numpy as np

from app_parameters import app_parameters

# IS_TESTING = True
IS_TESTING = False


def process_test_coverage(pipe, center_freq, stop_pipe):
    # read in fft data
    fft_data = []
    with open('C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data.txt') as f:
        fft_data = f.readlines()
        fft_data = [float(x.strip()) for x in fft_data]

    # process to dbm data
    signal_data = [20*math.log10(2*x / 1024) for x in fft_data]

    while True:
        if IS_TESTING:
            pipe.send(signal_data)
            if stop_pipe.poll(timeout=0):
                stop_pipe.recv()
                return
            time.sleep(3)


def process_test_recording(pipe, center_freq, stop_pipe):
    # read in fft data
    fft_data = []
    with open('C:/Users/65844/Desktop/citrus/exploration/3dplot_data/data.txt') as f:
        fft_data = f.readlines()
        fft_data = [float(x.strip()) for x in fft_data]

    # process to dbm data
    signal_data = [20*math.log10(2*x / 1024) for x in fft_data]

    while True:
        if IS_TESTING:
            pipe.send(signal_data)
            if stop_pipe.poll(timeout=0):
                stop_pipe.recv()
                return
            time.sleep(3)


def process_once_spectrum_test(center_freq, bandwidth, output_queue):
    data = np.load(app_parameters.COVERAGE_SDR_TEST_DATA_PATH)
    output_queue.put(data.tolist())
    print("Exiting process_once_spectrum_test...")
    return
