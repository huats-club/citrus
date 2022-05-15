class FileNameUtil:
    def __init__(self):
        pass

    @staticmethod
    def createFilepath(dirpath, name, uuid, ext="jpg"):
        return f"{dirpath}/{name}_{uuid}.{ext}"

    @staticmethod
    def createHeatmapFilepath(dirpath, name, uuid, ext="jpg"):
        return f"{dirpath}/{name}_{uuid}.{ext}"
