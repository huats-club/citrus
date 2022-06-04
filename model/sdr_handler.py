import time
from multiprocessing import Pipe, Process

import pycitrus


class SDRHandler:
    def __init__(self, driver_name):
        # Create stop pipes for process
        self.stop_pipe_handler,  self.stop_pipe_process = Pipe(True)
        self.data_pipe_handler,  self.data_pipe_process = Pipe(True)
        self.driver_name = driver_name

    def start(self, center_freq, bandwidth, sample_rate):
        # Define process for spectrum analyzer first
        self.process_spectrum_analyzer = Process(target=process_spectrum, daemon=True, args=(
            self.driver_name, center_freq, bandwidth, sample_rate, self.stop_pipe_process, self.data_pipe_process, ))
        self.process_spectrum_analyzer.start()

    def get_output_pipe(self):
        return self.data_pipe_handler

    def stop(self):
        self.stop_pipe_handler.send("stop")


def process_spectrum(
        driver_name, center_freq, bandwidth, sample_rate, stop_pipe, data_out_pipe, extensions=0.5 * 1e6, tdelta=0.05):

    # flag to check if run should occur
    isRun = True

    # create citrus processor
    p = pycitrus.CitrusProcessor(center_freq, bandwidth + extensions, sample_rate)
    p.init(driver_name)

    # time check
    prev = time.time()

    while isRun:
        now = time.time()

        if now - prev > tdelta:
            out = p.run()

            try:
                data_out_pipe.send(out)
            except BrokenPipeError:
                break

            prev = time.time()

        if stop_pipe.poll(timeout=0):
            print("stop in process_spectrum")
            break

    p.close()
    print("Exiting process_spectrum...")
    return
