import tkinter as tk
from tkinter import ttk

from app_parameters import app_parameters
from view.main.coverage_mode.Coverage import CoveragePage
from view.main.recording_mode.Recording import RecordingPage
from view.main.replay_mode.Replay import ReplayPage
from view.main.spectrum_mode.Spectrum import SpectrumPage


class MainPage(ttk.Notebook):
    def __init__(self, parent, controller, spectrum_pipe, recording_pipe, session, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.spectrum_pipe = spectrum_pipe
        self.recording_pipe = recording_pipe
        self.session = session
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
            self.session,
            width=app_parameters.APP_WIDTH,
            height=app_parameters.APP_HEIGHT
        )

        # Add Spectrum Analyzer tab
        self.spectrum_page = SpectrumPage(
            self,
            self.controller,
            self.spectrum_pipe,
            self.session,
            width=app_parameters.APP_WIDTH,
            height=app_parameters.APP_HEIGHT
        )

        # Add recording tab
        self.recording_page = RecordingPage(
            self,
            self.controller,
            self.recording_pipe,
            width=app_parameters.APP_WIDTH,
            height=app_parameters.APP_HEIGHT
        )

        # Add replay tab
        self.replay_page = ReplayPage(
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
        self.add(
            self.replay_page,
            text=app_parameters.MODE_REPLAY
        )

        # Temporarily select spectrum analyzer as main
        self.select(self.coverage_page)

    def disable_toggle_tab(self):
        for tab_id in self.tabs():
            if tab_id != self.select():
                self.tab(tab_id, state='disabled')

    def enable_toggle_tab(self):
        for tab_id in self.tabs():
            self.tab(tab_id, state='normal')

    def setup_coverage_from_config(self, config_dict):
        self.coverage_page.setup_page_from_config(config_dict)

    def setup_spectrum_page_from_config(self, config, path):
        self.spectrum_page.setup_page_from_config(config, path)
