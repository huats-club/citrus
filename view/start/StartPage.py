import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from app_parameters import app_parameters
from view.start.InterfaceFrame import InterfaceFrame
from view.start.ProjectFrame import ProjectFrame


class StartPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        super().__init__(self.parent, *args, **kwargs)
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
            text="Welcome to " + app_parameters.APP_TITLE,
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
        self.project_container.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True  # ensures that the panel file out the the parent
        )
        self.project_frame = ProjectFrame(self.project_container)

        # Bottom most container
        self.bottom = tk.Frame(
            self.container
        )
        self.bottom.pack(
            padx=10,
            pady=5,
            side=tk.BOTTOM,
            fill=tk.BOTH,
            expand=True
        )

        # Label for error messages
        self.error_text = tk.StringVar()
        self.error_message_label = ttk.Label(
            self.bottom,
            style="danger.TLabel",
            textvariable=self.error_text
        )
        self.error_message_label.pack(
            side=tk.LEFT
        )

        # Start app button
        self.start_button = ttk.Button(
            self.bottom,
            style="primary.Outline.TButton",
            text="Start",
            command=self.controller.on_start_button_press
        )
        self.start_button.pack(
            anchor=tk.NW,
            side=tk.RIGHT
        )

    def get_project_settings(self):
        return self.project_frame.get_selection()

    def display_error_message(self):
        self.error_text.set("Error! Configurations incomplete.")
        self.error_message_label.after(5000, self.clear_error_message)

    def clear_error_message(self):
        self.error_text.set("")
