"""
GUI Dialogs Package

This package contains all dialog components for the PPT Translator GUI.
"""

__version__ = "1.0.0"
__author__ = "PPT Translator Team"

# Import dialog components for easy access
from .settings_dialog import SettingsDialog
from .api_key_dialog import ApiKeyDialog

__all__ = ["SettingsDialog", "ApiKeyDialog"]
