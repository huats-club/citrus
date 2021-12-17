import tkinter as tk
from tkinter import ttk

from app_util.app_util import resource_path
from PIL import Image, ImageTk
from view.main.SavePane import SavePane


class CoverageBar(ttk.Frame):
    def __init__(self, parent, controller, owner, * args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.owner = owner

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        # String length for button
        self.STRING_LENGTH = 10

        # Container for view utilties
        self.view_container = ttk.Frame(self)
        self.view_container.pack(
            padx=5,
            pady=5,
            side=tk.LEFT,
            anchor=tk.NW
        )

        # Container for plot utilities
        self.plot_container = ttk.Frame(self)
        self.plot_container.pack(
            padx=5,
            pady=5,
            side=tk.RIGHT,
            anchor=tk.NE
        )

        # Create save pane
        self.save_pane = SavePane(self, self.controller, self.owner, tk.RIGHT, pady=(0, 0))

        # Create combine button
        self.combine_button = ttk.Button(
            self.plot_container,
            style="primary.Outline.TButton",
            text="Combine".center(self.STRING_LENGTH, ' '),
            command=self.controller.display_heatmap
        )
        self.combine_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=5
        )

        # Create left button
        left_arrow_image = ImageTk.PhotoImage(
            Image.open(resource_path("assets/left-arrow.png")).resize((35, 35)))
        self.left_arrow_button = tk.Button(
            self.plot_container,
            text="",
            image=left_arrow_image,
            compound=tk.RIGHT
        )
        self.left_arrow_button.photo = left_arrow_image
        self.left_arrow_button.pack(
            expand=True,
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Create right button
        right_arrow_image = ImageTk.PhotoImage(
            Image.open(resource_path("assets/right-arrow.png")).resize((35, 35)))
        self.right_arrow_button = tk.Button(
            self.plot_container,
            text="",
            image=right_arrow_image,
            compound=tk.RIGHT
        )
        self.right_arrow_button.photo = right_arrow_image
        self.right_arrow_button.pack(
            expand=True,
            side=tk.RIGHT,
            padx=10,
            pady=5
        )
