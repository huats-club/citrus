import multiprocessing
import os
import tkinter as tk
from datetime import datetime

from ttkbootstrap import Style

from app_parameters import app_parameters
from controller import Controller
from model.Session import Session

# Start running GUI
if __name__ == "__main__":
    # To fix the multiple tkinter window spawning problem
    multiprocessing.freeze_support()

    # Generate overall workspace folder
    if not os.path.exists(app_parameters.WORKSPACE_FOLDER):
        os.mkdir(app_parameters.WORKSPACE_FOLDER)

    # Check folder path for user data
    session_name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    session_workspace_folder_relative = app_parameters.WORKSPACE_FOLDER + f"/{session_name}"
    os.mkdir(session_workspace_folder_relative)

    # Generate private cached folder
    session_workspace_private_relative = session_workspace_folder_relative + f"/cached"
    os.mkdir(session_workspace_private_relative)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    style = Style(theme=app_parameters.APP_THEME)  # https://ttkbootstrap.readthedocs.io/en/latest/themes.html

    # Create session
    session = Session(
        session_name,
        session_workspace_folder_relative,
        session_workspace_private_relative
    )
    controller = Controller(root, session)

    # Handle save session when tkinter app exits gracefully
    root.protocol("WM_DELETE_WINDOW", lambda: controller.on_exit(root))

    # Start Tk GUI in main thread
    root.mainloop()
