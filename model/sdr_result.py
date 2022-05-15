from model.scan_result import ScanResult


class SdrResult(ScanResult):
    def __init__(self):
        super().__init__()

    # Override
    def getUuid(self):
        pass

    # Override
    def getName(self):
        pass

    # Override
    def getStrength(self):
        pass
