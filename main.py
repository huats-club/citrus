import os
import tkinter as tk

from ttkbootstrap import Style

import AppParameters as app_params
from controller import Controller

# Start running GUI
if __name__ == "__main__":

    # Check folder path for user data
    if not os.path.exists(app_params.WORKSPACE_FOLDER):
        os.makedirs(app_params.WORKSPACE_FOLDER)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    style = Style(theme=app_params.APP_THEME)  # https://ttkbootstrap.readthedocs.io/en/latest/themes.html
    Controller(root)

    # Start Tk GUI in main thread
    root.mainloop()
