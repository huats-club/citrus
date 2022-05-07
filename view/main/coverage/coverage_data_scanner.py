import tkinter as tk
import tkinter.ttk as ttk

from view.main.coverage.sdr_tab.sdr_tab import CoverageSdrTab
from view.main.coverage.wifi_tab.wifi_tab import CoverageWifiTab
from view.main.select_driver_pane import SelectDriverPane


class CoverageDataScanner(ttk.Frame):
    def __init__(self, parent, controller, coverage, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.coverage = coverage

        # iid for entries
        self.idx = 0

        # is first run
        self.is_first_scan = True
        self.sdr_handler = None

        self.calibrate_data = None

        super().__init__(
            self.parent,
            # text="Data Scanner",
            *args, **kwargs
        )
        self.pack(
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.X
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Create select driver
        self.select_driver_pane = SelectDriverPane(self, self.controller)

        # create notebook to choose interface
        self.interfaces_selection = ttk.Notebook(
            self,
            style="primary.TNotebook",
            * args, **kwargs
        )
        self.interfaces_selection.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Add SDR tab
        self.sdr_tab = CoverageSdrTab(
            self.interfaces_selection,
            self.controller,
            self.coverage
        )

        # Add Wifi tab
        self.wifi_tab = CoverageWifiTab(
            self.interfaces_selection,
            self.controller,
            self.coverage
        )

        self.interfaces_selection.add(
            self.wifi_tab,
            text="WIFI"
        )
        self.interfaces_selection.add(
            self.sdr_tab,
            text="SDR"
        )

        # Select wifi as main tab
        self.interfaces_selection.select(self.wifi_tab)

        # note when notebook tab change
        self.interfaces_selection.bind('<<NotebookTabChanged>>', self.switch_SDR_2_wifi_tab)

    def switch_SDR_2_wifi_tab(self, a):
        pass
