import multiprocessing
import os
import tkinter as tk
from datetime import datetime

from ttkbootstrap import Style

import config.app_parameters as app_parameters
from controller import Controller
from model.session import Session

# Start running GUI
if __name__ == "__main__":
    # To fix the multiple tkinter window spawning problem
    multiprocessing.freeze_support()

    # Generate overall workspace folder
    if not os.path.exists(app_parameters.WORKSPACE_FOLDER):
        os.mkdir(app_parameters.WORKSPACE_FOLDER)
        print(f"Workspace root folder doesn't exist, creating folder {app_parameters.WORKSPACE_FOLDER}")

    # Check folder path for user data
    session_name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    session_workspace_folder_relative = app_parameters.WORKSPACE_FOLDER + f"/{session_name}"
    os.mkdir(session_workspace_folder_relative)
    print(f"Created session folder: {session_workspace_folder_relative}")

    # Generate private cached folder
    session_workspace_private_relative = session_workspace_folder_relative + f"/cached"
    os.mkdir(session_workspace_private_relative)
    print(f"Created private cache folder: {session_workspace_private_relative}")

    # Create session object
    session = Session(session_name, session_workspace_folder_relative, session_workspace_private_relative)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    style = Style(theme=app_parameters.APP_THEME)  # https://ttkbootstrap.readthedocs.io/en/latest/themes.html

    # Configure root page properties
    root.resizable(width=False, height=False)    # Don't allow resizing
    root.title(app_parameters.APP_TITLE)
    root.iconbitmap(app_parameters.APP_ICO_PATH)

    # Create controller object
    controller = Controller(root, session)

    # Handle save session when tkinter app exits gracefully
    root.protocol("WM_DELETE_WINDOW", lambda: controller.on_exit())

    # Start Tk GUI in main thread
    root.mainloop()
