import multiprocessing
import os
import tkinter as tk
from datetime import datetime

from ttkbootstrap import Style

from app_parameters import app_parameters
from controller import Controller

# Start running GUI
if __name__ == "__main__":
    # To fix the multiple tkinter window spawning problem
    multiprocessing.freeze_support()

    # Generate overall workspace folder
    if not os.path.exists(app_parameters.WORKSPACE_FOLDER):
        os.mkdir(app_parameters.WORKSPACE_FOLDER)

    # Check folder path for user data
    session_name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    app_parameters.WORKSPACE_FOLDER = app_parameters.WORKSPACE_FOLDER + f"/{session_name}"
    os.mkdir(app_parameters.WORKSPACE_FOLDER)

    # Generate private cached folder
    app_parameters.PRIVATE_FOLDER = app_parameters.WORKSPACE_FOLDER + f"/cached"
    os.mkdir(app_parameters.PRIVATE_FOLDER)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    style = Style(theme=app_parameters.APP_THEME)  # https://ttkbootstrap.readthedocs.io/en/latest/themes.html
    controller = Controller(root, session_name)

    # Handle save session when tkinter app exits gracefully
    root.protocol("WM_DELETE_WINDOW", lambda: controller.on_exit(root))

    # Start Tk GUI in main thread
    root.mainloop()
