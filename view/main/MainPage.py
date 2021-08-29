import tkinter as tk
from tkinter import ttk

import AppParameters as app_params
from view.main.Spectrum import SpectrumPage


class MainPage(ttk.Notebook):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        super().__init__(self.parent, *args, **kwargs)
        self.pack(
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Add Spectrum Analyzer tab
        self.spectrum_page = SpectrumPage(
            self,
            self.controller,
            width=app_params.APP_WIDTH,
            height=app_params.APP_HEIGHT
        )
        self.spectrum_page.pack()

        # Add tab 2
        self.tab2 = ttk.Frame(
            self,
            width=app_params.APP_WIDTH,
            height=app_params.APP_HEIGHT
        )
        self.tab2.pack()

        # Add tab 2
        self.tab3 = ttk.Frame(
            self,
            width=app_params.APP_WIDTH,
            height=app_params.APP_HEIGHT
        )
        self.tab3.pack()

        self.add(
            self.spectrum_page,
            text="Spectrum Mode"
        )
        self.add(
            self.tab2,
            text="One"
        )
        self.add(
            self.tab3,
            text="One"
        )
