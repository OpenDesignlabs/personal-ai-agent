#!/usr/bin/env python3
"""
Jarvis AI - Main Application Entry Point
Optimized for stability and performance
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys
import logging
from dotenv import dotenv_values
from Frontend.GUI import JarvisAIApp

# Configure logging for better error tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_environment():
    """Load environment variables with error handling"""
    try:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        env_vars = dotenv_values(env_path)
        
        # Validate required environment variables
        Username = env_vars.get("Username", "User")
        Assistantname = env_vars.get("Assistantname", "Jarvis")
        
        # Log successful loading
        logger.info(f"Environment loaded successfully for user: {Username}")
        return env_vars, Username, Assistantname
        
    except Exception as e:
        logger.error(f"Failed to load environment: {e}")
        # Return default values if env loading fails
        return {}, "User", "Jarvis"

def create_main_window():
    """Create and configure the main window with optimizations"""
    try:
        # Create root window with performance optimizations
        root = tk.Tk()
        
        # Window configuration
        root.title("Jarvis AI Assistant")
        root.geometry("800x600")
        root.minsize(600, 400)
        
        # Performance optimizations
        root.tk.call('tk', 'scaling', 1.0)  # Prevent scaling issues
        root.option_add('*tearOff', False)  # Disable tear-off menus
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        logger.info("Main window created successfully")
        return root
        
    except Exception as e:
        logger.error(f"Failed to create main window: {e}")
        raise

def initialize_application(root, env_vars, Username, Assistantname):
    """Initialize the Jarvis AI application"""
    try:
        # Initialize application with environment variables
        app = JarvisAIApp(root)
        
        # Set up window close protocol with proper cleanup
        def on_closing():
            try:
                logger.info("Application closing...")
                app.on_closing()
                root.destroy()
            except Exception as e:
                logger.error(f"Error during closing: {e}")
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        logger.info("Application initialized successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

def main():
    """Main function to run the Jarvis AI application"""
    try:
        logger.info("Starting Jarvis AI Application...")
        
        # Load environment variables
        env_vars, Username, Assistantname = load_environment()
        
        # Create main window
        root = create_main_window()
        
        # Initialize application
        app = initialize_application(root, env_vars, Username, Assistantname)
        
        # Start the main loop with error handling
        logger.info("Starting main loop...")
        root.mainloop()
        
        logger.info("Application closed successfully")
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
        
    except ImportError as e:
        error_msg = f"Missing required library: {str(e)}\nPlease install requirements: py -m pip install -r Requirements.txt"
        logger.error(error_msg)
        messagebox.showerror("Import Error", error_msg)
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Failed to start Jarvis AI: {str(e)}"
        logger.error(error_msg)
        messagebox.showerror("Application Error", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()