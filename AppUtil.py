import os
import sys
import time

import pandas as pd

from testing import IS_TESTING


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # pylint: disable=no-member
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def testing(pipe):

    print("opening file")
    df = pd.read_csv(r'out.csv')

    while True:
        if IS_TESTING:
            print("hello11")
            pipe.send(df['power'])
            time.sleep(10)
