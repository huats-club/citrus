import multiprocessing
import os
import tkinter as tk

from ttkbootstrap import Style

from app_parameters import app_parameters
from controller import Controller

# Start running GUI
if __name__ == "__main__":
    # To fix the multiple tkinter window spawning problem
    multiprocessing.freeze_support()

    # Check folder path for user data
    if not os.path.exists(app_parameters.WORKSPACE_FOLDER):
        os.makedirs(app_parameters.WORKSPACE_FOLDER)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    style = Style(theme=app_parameters.APP_THEME)  # https://ttkbootstrap.readthedocs.io/en/latest/themes.html
    Controller(root)

    # Start Tk GUI in main thread
    root.mainloop()
