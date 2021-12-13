import time

import pycitrus


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
