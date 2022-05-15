import math
from multiprocessing import Pipe, Process, Queue

import numpy as np

from model.coverage_util import process_once_spectrum


class CoverageSingleHandler:
    def __init__(self, driver_name, calibrate_data):
        self.driver_name = driver_name
        # Calibrate data
        self.calibrate_data = calibrate_data
        self.is_calibrating = False

    def start(self, center_freq, bandwidth, sample_rate):
        # Create pipes for coverage process
        get_pipe_coverage_data_scanner, get_pipe_process = Pipe(True)
        self.get_pipe_coverage_data_scanner = get_pipe_coverage_data_scanner
        self.get_pipe_process = get_pipe_process

        # Create pipes for coverage process
        stop_pipe_coverage_data_scanner, stop_pipe_process = Pipe(True)
        self.stop_pipe_coverage_data_scanner = stop_pipe_coverage_data_scanner
        self.stop_pipe_process = stop_pipe_process

        # Pipe to go into process
        self.spectrum_queue = Queue()

        # Define process for spectrum analyzer first
        self.process_spectrum_analyzer = Process(target=process_once_spectrum, daemon=True, args=(
            center_freq, bandwidth, sample_rate, self.spectrum_queue, self.get_pipe_process, self.stop_pipe_process,))

        self.process_spectrum_analyzer.start()

    def get_result(self):
        # send signal to process to get data
        self.get_pipe_coverage_data_scanner.send("")

        fft_data = self.spectrum_queue.get(timeout=100)
        average_of_all_calibrate = np.average(fft_data)
        fft_data = np.subtract(fft_data, self.calibrate_data)
        fft_data = fft_data + average_of_all_calibrate

        for idx in range(len(fft_data)):
            if fft_data[idx] < 0:
                fft_data[idx] = average_of_all_calibrate

        # Compute RSSI from data
        dbm_data = [20*math.log10(2*x / 1024) for x in fft_data]
        return dbm_data

    def close(self):
        self.stop_pipe_coverage_data_scanner.send("")
        self.process_spectrum_analyzer.join()
        self.process_spectrum_analyzer.close()
