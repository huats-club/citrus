from AppUtil import resource_path

### Main App parameters ###
WORKSPACE_FOLDER = 'workspace'
APP_HEIGHT = 300
APP_WIDTH = 900
APP_TITLE = "Citrus"
APP_ICO_PATH = resource_path("assets/seedling.ico")
APP_THEME = 'sandstone'

PROJECT_NEW = "NEW"
PROJECT_LOAD = "LOAD"
INTERFACE_WIFI = "WIFI CHIP"
INTERFACE_SDR = "LIMESDR MINI"
INTERFACE_LIST = (INTERFACE_WIFI, INTERFACE_SDR)

MODE_SPECTRUM_ANALYZER = "Spectrum Mode"
MODE_RECORDING = "Recording Mode"
MODE_COVERAGE = "Coverage Mode"
