import os
import tkinter as tk

from ttkbootstrap import Style

import AppParameters as app_params
from Controller import Controller

# Start running GUI
if __name__ == "__main__":

    # Check folder path for user data
    if not os.path.exists(app_params.WORKSPACE_FOLDER):
        os.makedirs(app_params.WORKSPACE_FOLDER)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    style = Style(theme='sandstone')  # https://ttkbootstrap.readthedocs.io/en/latest/themes.html
    Controller(root)

    # Start Tk GUI in main thread
    root.mainloop()
