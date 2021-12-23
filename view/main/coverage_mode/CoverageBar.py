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

        # list of heatmaps
        self.heatmaps = ["".center(30, ' ')]

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

        # Create toggle button for Create heatmap
        self.create_text = tk.StringVar()
        self.create_text.set('Create'.center(self.STRING_LENGTH, ' '))

        self.create_button = ttk.Button(
            self.plot_container,
            style="primary.Outline.TButton",
            textvariable=self.create_text,
            command=self.controller.display_heatmap
        )
        self.create_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # label to indicate which heatmap to choose
        self.heatmap_choose_label = tk.Label(
            self.plot_container, text="View:")
        self.heatmap_choose_label.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        # Option to choose which heatmap to view
        self.heatmap_value_menu = tk.StringVar()
        self.heatmap_value_menu.set(self.heatmaps[0])
        self.heatmap_menu = ttk.OptionMenu(
            self.plot_container,
            self.heatmap_value_menu,
            *self.heatmaps
        )
        self.heatmap_menu.pack(side=tk.RIGHT)
