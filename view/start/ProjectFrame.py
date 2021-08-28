import tkinter as tk
from tkinter import ttk

import AppParameters as app_params


class ProjectFrame(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        # Create interface frame object
        super().__init__(
            self.parent,
            style="info.inverse.TLabelframe",
            text="Project Workspace",
            width=app_params.APP_WIDTH / 2,
            height=app_params.APP_HEIGHT / 2  # todo: remove this later
        )
        self.pack(
            side=tk.BOTTOM,
            padx=8,
            pady=8
        )
