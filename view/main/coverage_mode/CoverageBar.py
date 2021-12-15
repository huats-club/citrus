import tkinter as tk
from tkinter import ttk

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
