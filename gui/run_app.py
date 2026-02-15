"""Entry point for PPT Translator GUI application.

This module serves as the main entry point when running the application
as a standalone executable. It properly initializes the package context
and launches the main window.
"""

import sys
import os

# Add the parent directory to Python path for proper package imports
# This ensures that 'gui' package can be imported correctly
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = os.path.dirname(sys.executable)
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(application_path)
    if parent_path not in sys.path:
        sys.path.insert(0, parent_path)

# Now import and run the main application
from gui.main_window import MainWindow
import customtkinter as ctk


def main():
    """Main entry point for the application."""
    # Set theme and appearance
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    # Create and run the main window
    app = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
