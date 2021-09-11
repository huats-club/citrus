import time

import pandas as pd

IS_TESTING = True
# IS_TESTING = False


def process_test(pipe, center_freq, stop_pipe):
    df = pd.read_csv(r'out.csv')

    while True:
        if IS_TESTING:
            pipe.send(df['power'])
            if stop_pipe.poll(timeout=0):
                stop_pipe.recv()
                return
            time.sleep(5)
