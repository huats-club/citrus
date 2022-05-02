import random
from multiprocessing import Pipe, Process, Queue

from model.CalibrateHandler import CalibrateHandlerBlock
from testing import (IS_TESTING, process_once_spectrum_test,
                     process_test_coverage)

from model.CoverageUtil import process_once_spectrum, process_spectrum
import math
import numpy as np


class CoverageHandler:
    def __init__(self, driver_name):
        # Create stop pipes for process
        stop_pipe_handler, stop_pipe_process = Pipe(True)
        self.stop_pipe_process = stop_pipe_process
        self.stop_pipe_handler = stop_pipe_handler

        self.driver_name = driver_name

    def start(self, pipe, center_freq, bandwidth):
        if not IS_TESTING:
            # Define process for spectrum analyzer first
            self.process_spectrum_analyzer = Process(
                target=process_spectrum, daemon=True,
                args=(self.driver_name, pipe, center_freq, bandwidth, self.stop_pipe_process,))
        else:
            # Define mock process
            self.process_spectrum_analyzer = Process(
                target=process_test_coverage, daemon=True,
                args=(pipe, center_freq, self.stop_pipe_process,))

        self.process_spectrum_analyzer.start()

    def stop(self):
        self.stop_pipe_handler.send("stop")


class CoverageSingleHandler:
    def __init__(self, driver_name):
        self.driver_name = driver_name
        # Calibrate data
        self.calibrate_data = None
        self.is_calibrating = False

    def start(self, center_freq, bandwidth):

        # Do calibration
        c = CalibrateHandlerBlock()
        self.calibrate_data = c.start(self.driver_name, center_freq, bandwidth)

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

        if not IS_TESTING:
            # Define process for spectrum analyzer first
            self.process_spectrum_analyzer = Process(
                target=process_once_spectrum, daemon=True,
                args=(center_freq, bandwidth, self.spectrum_queue, self.get_pipe_process, self.stop_pipe_process,))
        else:
            # Define mock process
            self.process_spectrum_analyzer = Process(
                target=process_once_spectrum_test, daemon=True, args=(None, center_freq, self.spectrum_queue, ))

        self.process_spectrum_analyzer.start()

    def get_result(self):
        if not IS_TESTING:

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

        else:
            return [random.randrange(-50, -5) for _ in range(2048)]

    def close(self):
        self.stop_pipe_coverage_data_scanner.send("")
        self.process_spectrum_analyzer.join()
        self.process_spectrum_analyzer.close()
