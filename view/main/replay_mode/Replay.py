import tkinter as tk
from tkinter import ttk

from view.main.replay_mode.ReplayPlot import ReplayPlot
from view.main.replay_mode.ReplaySettingPane import ReplaySettingPane


class ReplayPage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent,  *args, **kwargs)
        self.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True
        )

        # Create plot container
        self.plot_container = tk.Frame(
            self.container
        )
        self.plot_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )

        # Create plot object
        self.plot = ReplayPlot(self.plot_container, self.controller)

        # Bottom container
        self.settings_container = tk.Frame(
            self.container
        )
        self.settings_container.pack(
            padx=10,
            pady=10,
            side=tk.BOTTOM,
            fill=tk.BOTH
        )

        # Create replay settings
        self.replay_settings_pane = ReplaySettingPane(self.settings_container, self, self.controller)
