import multiprocessing
import tkinter as tk

from ttkbootstrap import Style

import config.app_parameters as app_parameters
from controller import Controller

# Start running GUI
if __name__ == "__main__":
    # To fix the multiple tkinter window spawning problem
    multiprocessing.freeze_support()

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    style = Style(theme=app_parameters.APP_THEME)  # https://ttkbootstrap.readthedocs.io/en/latest/themes.html

    # Configure root page properties
    root.resizable(width=False, height=False)    # Don't allow resizing
    root.title(app_parameters.APP_TITLE)
    root.iconbitmap(app_parameters.APP_ICO_PATH)

    # Create controller object
    controller = Controller(root)

    # Handle save session when tkinter app exits gracefully
    root.protocol("WM_DELETE_WINDOW", lambda: controller.on_exit())

    # Start Tk GUI in main thread
    root.mainloop()
