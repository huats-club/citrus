from multiprocessing import Pipe, Process

from model.WifiUtil import process_wifi


class WifiHandler:
    def __init__(self, tracked_list_mac, pipe):
        self.tracked_list_mac = tracked_list_mac
        self.process_lswifi_tracker = Process(
            target=process_wifi, daemon=True, args=(self.tracked_list_mac, pipe,))

    def start(self):
        self.process_lswifi_tracker.start()
