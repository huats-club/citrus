import tkinter as tk
from tkinter import ttk

import AppParameters as app_params
from view.main.Spectrum import SpectrumPage


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
        self.coverage_page = ttk.Frame(
            self,
            width=app_params.APP_WIDTH,
            height=app_params.APP_HEIGHT
        )
        self.coverage_page.pack()

        # Add Spectrum Analyzer tab
        self.spectrum_page = SpectrumPage(
            self,
            self.controller,
            width=app_params.APP_WIDTH,
            height=app_params.APP_HEIGHT
        )
        self.spectrum_page.pack()

        # Add recording tab
        self.recording_page = ttk.Frame(
            self,
            width=app_params.APP_WIDTH,
            height=app_params.APP_HEIGHT
        )
        self.recording_page.pack()

        self.add(
            self.coverage_page,
            text=app_params.MODE_COVERAGE
        )
        self.add(
            self.spectrum_page,
            text=app_params.MODE_SPECTRUM_ANALYZER
        )
        self.add(
            self.recording_page,
            text=app_params.MODE_RECORDING
        )

        # Temporarily select spectrum analyzer as main
        self.select(self.spectrum_page)