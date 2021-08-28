import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import AppParameters as app_params


class Landing(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller

        # Main container
        self.container = tk.Frame(self.parent)
        self.container.pack(padx=10, pady=10)

        # Introduction label
        self.introduction_label_container = tk.Frame(self.container)
        self.introduction_label_container.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH
        )
        welcome_fontStyle = tkFont.Font(
            family="TkDefaultFont", size=18, weight="bold")
        self.introduction_label = ttk.Label(
            self.introduction_label_container,
            text="Welcome to " + app_params.APP_TITLE,
            # style='info.TLabel',
            font=welcome_fontStyle,
            anchor=tk.CENTER
        )
        self.introduction_label.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )

        # Load project panel
        self.project_container = tk.Frame(self.container)
        self.project_container.pack(side=tk.TOP)

        self.project_frame = ttk.LabelFrame(
            self.project_container,
            # style="info.TLabelframe",
            text="Project Workspace",
            width=app_params.APP_WIDTH / 2,
            height=app_params.APP_HEIGHT / 2  # todo: remove this later
        )
        self.project_frame.pack(side=tk.TOP)

        # Select Interface panel
        self.interface_container = tk.Frame(self.container)
        self.interface_container.pack(side=tk.TOP)

        self.interface_frame = ttk.LabelFrame(
            self.interface_container,
            # style="info.TLabelframe",
            text="Select interface",
            width=app_params.APP_WIDTH / 2,
            height=app_params.APP_HEIGHT / 2  # todo: remove this later
        )
        self.interface_frame.pack(side=tk.TOP)
