import time

import numpy as np
import pycitrus
from app_parameters import app_parameters


def process_spectrum(pipe, center_freq, bandwidth, stop_pipe):

    # flag to check if run should occur
    isRun = True

    # create citrus processor
    p = pycitrus.CitrusProcessor(center_freq, bandwidth)
    p.init()

    # time check
    prev = time.time()

    while isRun:
        now = time.time()

        if now - prev > 0.8:
            out = p.run()
            pipe.send(out)
            prev = time.time()

        if stop_pipe.poll(timeout=0):
            print("stop in process")
            stop_pipe.recv()
            isRun = False
            p.close()

    print("Exiting process_spectrum...")
    return


def process_once_spectrum(center_freq, bandwidth, output_queue):

    # create citrus processor
    p = pycitrus.CitrusProcessor(center_freq, bandwidth)
    p.init()
    out = p.run()
    p.close()

    # queue the output data back
    output_queue.put(out)

    print("Exiting process_once_spectrum...")
    return


def process_once_spectrum_test(center_freq, bandwidth, output_queue):
    data = np.load(app_parameters.COVERAGE_SDR_TEST_DATA_PATH)
    output_queue.put(data.tolist())
    print("Exiting process_once_spectrum_test...")
    return
