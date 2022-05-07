import tkinter as tk
from tkinter import ttk

import config.app_parameters as app_parameters
from view.main.coverage.coverage import CoveragePage
from view.main.recording.recording import RecordingPage
from view.main.spectrum.spectrum import SpectrumPage


class MainPage(ttk.Notebook):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        super().__init__(
            self.parent,
            style="primary.TNotebook",
            * args, **kwargs
        )
        self.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )
        self.enable_traversal()  # Enable using keyboard to traverse tab

        # Add coverage tab
        self.coverage_page = CoveragePage(
            self,
            self.controller,
            width=app_parameters.APP_WIDTH,
            height=app_parameters.APP_HEIGHT
        )

        # Add Spectrum Analyzer tab
        self.spectrum_page = SpectrumPage(
            self,
            self.controller,
            width=app_parameters.APP_WIDTH,
            height=app_parameters.APP_HEIGHT
        )

        # Add recording tab
        self.recording_page = RecordingPage(
            self,
            self.controller,
            width=app_parameters.APP_WIDTH,
            height=app_parameters.APP_HEIGHT
        )

        self.add(
            self.coverage_page,
            text=app_parameters.MODE_COVERAGE
        )
        self.add(
            self.spectrum_page,
            text=app_parameters.MODE_SPECTRUM_ANALYZER
        )
        self.add(
            self.recording_page,
            text=app_parameters.MODE_RECORDING
        )

        # Temporarily select Coverage as main
        self.select(self.spectrum_page)
