from multiprocessing import Pipe, Process

from AppUtil import process_spectrum, process_test
from testing import IS_TESTING


class SDRHandler:
    def __init__(self):
        # Create stop pipes for process
        stop_pipe_handler, stop_pipe_process = Pipe(True)
        self.stop_pipe_process = stop_pipe_process
        self.stop_pipe_handler = stop_pipe_handler

    def start(self, pipe, center_freq):
        if not IS_TESTING:
            # Define process for spectrum analyzer first
            self.process_spectrum_analyzer = Process(
                target=process_spectrum, daemon=True, args=(pipe, center_freq, self.stop_pipe_process,))
        else:
            # Define mock process
            self.process_spectrum_analyzer = Process(
                target=process_test, daemon=True, args=(pipe, center_freq, self.stop_pipe_process,))

        self.process_spectrum_analyzer.start()

    def stop(self):
        self.stop_pipe_handler.send("stop")
