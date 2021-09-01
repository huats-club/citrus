import time

import pandas as pd

# IS_TESTING = True
IS_TESTING = False


def process_test(pipe, center_freq, stop_pipe):

    print("opening file")
    df = pd.read_csv(r'out.csv')

    while True:
        if IS_TESTING:
            print("hello11")
            pipe.send(df['power'])

            if stop_pipe.poll(timeout=0):
                print("stop in process")
                stop_pipe.recv()
                return

            time.sleep(5)
