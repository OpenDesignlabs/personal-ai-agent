#!/usr/bin/env python3
"""
Jarvis AI - Prime Entry Point
Redesigned for a Premium Experience
"""

import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import logging
from dotenv import dotenv_values
from Frontend.GUI import JarvisAIApp

# --- Global Configurations ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('jarvis.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def load_environment():
    try:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        env_vars = dotenv_values(env_path)
        return env_vars, env_vars.get("Username", "User"), env_vars.get("Assistantname", "Jarvis")
    except Exception as e:
        logger.error(f"Env Load Failure: {e}")
        return {}, "User", "Jarvis"

def main():
    try:
        logger.info("Initializing Jarvis AI Prime...")
        env_vars, username, assistant_name = load_environment()

        # Create root window using CustomTkinter for modern behavior
        root = ctk.CTk()
        root.title(f"{assistant_name} - Autonomous Intelligence")
        
        # Window size & Centering
        window_width = 1400
        window_height = 900
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Design Attributes
        # root.attributes("-alpha", 0.98) # Option removed for stability in Prime UI
        
        # Initialize the Redesigned App
        app = JarvisAIApp(root)
        
        def on_closing():
            if messagebox.askokcancel("Terminate", "Are you sure you want to take Jarvis offline?"):
                app.on_closing()
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        logger.info("Main loop engaged.")
        root.mainloop()

    except Exception as e:
        logger.critical(f"Kernel Panic: {e}")
        messagebox.showerror("Critical Failure", f"Jarvis encountered a core error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()