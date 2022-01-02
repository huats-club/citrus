import random
from multiprocessing import Pipe, Process, Queue

from testing import (IS_TESTING, process_once_spectrum_test,
                     process_test_coverage)

from model.CoverageUtil import process_once_spectrum, process_spectrum


class CoverageHandler:
    def __init__(self):
        # Create stop pipes for process
        stop_pipe_handler, stop_pipe_process = Pipe(True)
        self.stop_pipe_process = stop_pipe_process
        self.stop_pipe_handler = stop_pipe_handler

    def start(self, pipe, center_freq, bandwidth):
        if not IS_TESTING:
            # Define process for spectrum analyzer first
            self.process_spectrum_analyzer = Process(
                target=process_spectrum, daemon=True,
                args=(pipe, center_freq, bandwidth, self.stop_pipe_process,))
        else:
            # Define mock process
            self.process_spectrum_analyzer = Process(
                target=process_test_coverage, daemon=True,
                args=(pipe, center_freq, self.stop_pipe_process,))

        self.process_spectrum_analyzer.start()

    def stop(self):
        self.stop_pipe_handler.send("stop")


class CoverageSingleHandler:
    def __init__(self):
        pass

    def start(self, center_freq, bandwidth):
        self.queue = Queue()

        # Create pipes for coverage process
        get_pipe_coverage_data_scanner, get_pipe_process = Pipe(True)
        self.get_pipe_coverage_data_scanner = get_pipe_coverage_data_scanner
        self.get_pipe_process = get_pipe_process

        # Create pipes for coverage process
        stop_pipe_coverage_data_scanner, stop_pipe_process = Pipe(True)
        self.stop_pipe_coverage_data_scanner = stop_pipe_coverage_data_scanner
        self.stop_pipe_process = stop_pipe_process

        if not IS_TESTING:
            # Define process for spectrum analyzer first
            self.process_spectrum_analyzer = Process(
                target=process_once_spectrum, daemon=True,
                args=(center_freq, bandwidth, self.queue, self.get_pipe_process, self.stop_pipe_process,))
        else:
            # Define mock process
            self.process_spectrum_analyzer = Process(
                target=process_once_spectrum_test, daemon=True, args=(None, center_freq, self.queue, ))

        self.process_spectrum_analyzer.start()

    def get_result(self):
        if not IS_TESTING:

            # send signal to process to get data
            self.get_pipe_coverage_data_scanner.send("")

            return self.queue.get(timeout=100)
        else:
            return [random.randrange(-50, -5)for _ in range(2048)]

    # TODO
    def close(self):
        self.stop_pipe_coverage_data_scanner.send("")
        pass
