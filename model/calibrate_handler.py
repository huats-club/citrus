import time
from multiprocessing import Process

import numpy as np
import pycitrus


def process_calibrate(driver_name, pipe_out, center_freq, bandwidth, sample_rate):

    # create citrus processor
    p = pycitrus.CitrusProcessor(center_freq, bandwidth, sample_rate)
    p.init(driver_name)

    data = [0 for _ in range(2048)]

    for _ in range(20):
        out = p.run()

        data = np.add(data, out)

        time.sleep(0.05)

    data = data / 20.0
    pipe_out.send(data.tolist())

    p.close()
    return


class CalibrateHandler:
    def __init__(self):
        pass

    def start(self, driver_name, pipe, center_freq, bandwidth, sample_rate):
        self.process = Process(
            target=process_calibrate, daemon=True,
            args=(driver_name, pipe, center_freq, bandwidth, sample_rate))
        self.process.start()
