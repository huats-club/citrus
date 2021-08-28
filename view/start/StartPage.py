import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import AppParameters as app_params
from view.start.InterfaceFrame import InterfaceFrame
from view.start.ProjectFrame import ProjectFrame


class StartPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller

        # Main container
        self.container = tk.Frame(self.parent)
        self.container.pack(
            padx=10,
            pady=10
        )

        # Introduction label
        self.introduction_label_container = tk.Frame(self.container)
        self.introduction_label_container.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH
        )
        welcome_fontStyle = tkFont.Font(
            family="TkDefaultFont",
            size=18,
            weight="bold"
        )
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

        # Select Interface panel
        self.interface_container = tk.Frame(self.container)
        self.interface_container.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )
        self.interface_frame = InterfaceFrame(self.interface_container)

        # Load project panel
        self.project_container = tk.Frame(self.container)
        self.project_container.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )
        self.project_frame = ProjectFrame(self.project_container)

        # Start app button
        self.start_button = ttk.Button(
            self.container,
            style="info.Outline.TButton",
            text="Start",
            command=self.controller.onStartButtonPress
        )
        self.start_button.pack(
            side=tk.BOTTOM
        )
