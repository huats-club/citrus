import time

import pycitrus


def process_spectrum(driver_name, pipe, center_freq, bandwidth, stop_pipe):

    # flag to check if run should occur
    isRun = True

    # create citrus processor
    p = pycitrus.CitrusProcessor(center_freq, bandwidth)
    p.init(driver_name)

    # time check
    prev = time.time()

    while isRun:
        now = time.time()

        if now - prev > 0.4:
            out = p.run()
            pipe.send(out)
            prev = time.time()

        if stop_pipe.poll(timeout=0):
            print("stop in process")
            isRun = False
            p.close()

    print("Exiting process_spectrum...")
    return


def process_once_spectrum(center_freq, bandwidth, output_queue, get_pipe, stop_pipe):

    # flag to check if run should occur
    isRun = True

    # create citrus processor
    p = pycitrus.CitrusProcessor(center_freq, bandwidth)
    p.init("lime")

    while isRun:

        if get_pipe.poll(timeout=0):
            out = p.run()

            # queue the output data back
            output_queue.put(out)

            # remove signal
            get_pipe.recv()

        if stop_pipe.poll(timeout=0):
            p.close()
            isRun = False

    print("Exiting process_once_spectrum...")
    return
