from config.app_util import resource_path

WORKSPACE_FOLDER = r'workspace'
PRIVATE_FOLDER = r'workspace\cached'

### Main App parameters ###
APP_HEIGHT = 800
APP_WIDTH = 1500
APP_TITLE = "Citrus"
APP_ICO_PATH = resource_path("assets/seedling.ico")
APP_THEME = 'sandstone'

PROJECT_NEW = "NEW"
PROJECT_LOAD = "LOAD"

MODE_SPECTRUM_ANALYZER = "Spectrum Mode"
MODE_RECORDING = "Recording Mode"
MODE_COVERAGE = "Coverage Mode"

SPECTRUM_PLOT_TITLE = "Spectrum Analyzer"
SPECTRUM_PLOT_LEGEND_X = "Frequency"
SPECTRUM_PLOT_LEGEND_Y = "Signal Strength"
SPECTRUM_PLOT_UNITS_PREFIX_MEGA_X = "M"
SPECTRUM_PLOT_UNITS_PREFIX_KILO_X = "K"
SPECTRUM_PLOT_UNITS_PREFIX_GIGA_X = "G"
SPECTRUM_PLOT_UNITS_POSTFIX_X = "Hz"
SPECTRUM_PLOT_UNITSD_Y = "Signal Strength"

CANVAS_HEIGHT = 800
CANVAS_WIDTH = 1200

WATERFALL_PLOT_LEGEND_X = 'freq_bins'
WATERFALL_PLOT_LEGEND_Y = 'timestamps'
WATERFALL_PLOT_LEGEND_Z = 'strength'
