"""Theme manager for PPT Translator GUI.

Provides centralized theme management with support for dark and light modes,
color schemes, and font configurations.
"""

from typing import Dict, Optional, Callable
import customtkinter as ctk


class ThemeManager:
    """Manages application theme and styling.
    
    Provides centralized access to color schemes, fonts, and theme switching.
    Supports both dark and light modes with a modern, consistent design.
    
    Attributes:
        current_theme: Current theme mode ('dark' or 'light')
        colors: Dictionary of color values for current theme
        fonts: Dictionary of font configurations
        _observers: List of callback functions for theme change notifications
    
    Example:
        >>> theme_manager = ThemeManager()
        >>> theme_manager.set_theme('dark')
        >>> bg_color = theme_manager.get_color('bg_primary')
    """
    
    # Color schemes for dark theme
    DARK_THEME = {
        # Background colors
        'bg_primary': '#1a1a2e',      # Main background
        'bg_secondary': '#16213e',    # Card/section background
        'bg_tertiary': '#0f3460',     # Input/element background
        
        # Text colors
        'text_primary': '#eaeaea',    # Main text
        'text_secondary': '#a0a0a0',  # Secondary text
        'text_disabled': '#666666',   # Disabled text
        
        # Accent colors
        'accent_primary': '#e94560',  # Primary accent (buttons, highlights)
        'accent_secondary': '#0f3460', # Secondary accent
        'accent_hover': '#ff6b6b',    # Hover state
        
        # Status colors
        'success': '#4caf50',         # Success/green
        'warning': '#ff9800',         # Warning/orange
        'error': '#f44336',           # Error/red
        'info': '#2196f3',            # Info/blue
        
        # Border colors
        'border': '#2a2a4a',          # Default border
        'border_focus': '#e94560',    # Focused border
        'border_hover': '#3a3a6a',    # Hover border
    }
    
    # Color schemes for light theme
    LIGHT_THEME = {
        # Background colors
        'bg_primary': '#f5f5f7',      # Main background
        'bg_secondary': '#ffffff',    # Card/section background
        'bg_tertiary': '#e8e8ed',     # Input/element background
        
        # Text colors
        'text_primary': '#1d1d1f',    # Main text
        'text_secondary': '#86868b',  # Secondary text
        'text_disabled': '#c4c4c4',   # Disabled text
        
        # Accent colors
        'accent_primary': '#0071e3',  # Primary accent (buttons, highlights)
        'accent_secondary': '#5e5ce6', # Secondary accent
        'accent_hover': '#0077ed',    # Hover state
        
        # Status colors
        'success': '#34c759',         # Success/green
        'warning': '#ff9500',         # Warning/orange
        'error': '#ff3b30',           # Error/red
        'info': '#007aff',            # Info/blue
        
        # Border colors
        'border': '#d2d2d7',          # Default border
        'border_focus': '#0071e3',    # Focused border
        'border_hover': '#b8b8c0',    # Hover border
    }
    
    # Font configurations
    FONTS = {
        'heading_large': ('Segoe UI', 24, 'bold'),
        'heading_medium': ('Segoe UI', 18, 'bold'),
        'heading_small': ('Segoe UI', 14, 'bold'),
        'body_large': ('Segoe UI', 12, 'normal'),
        'body_medium': ('Segoe UI', 11, 'normal'),
        'body_small': ('Segoe UI', 10, 'normal'),
        'caption': ('Segoe UI', 9, 'normal'),
        'monospace': ('Consolas', 11, 'normal'),
    }
    
    def __init__(self, default_theme: str = 'dark'):
        """Initialize theme manager.
        
        Args:
            default_theme: Initial theme mode ('dark' or 'light')
        """
        self._current_theme = default_theme
        self._colors = self.DARK_THEME if default_theme == 'dark' else self.LIGHT_THEME
        self._fonts = self.FONTS.copy()
        self._observers: list[Callable[[str], None]] = []
        
        # Apply initial theme to CustomTkinter
        ctk.set_appearance_mode(default_theme)
        ctk.set_default_color_theme('dark-blue' if default_theme == 'dark' else 'blue')
    
    @property
    def current_theme(self) -> str:
        """Get current theme mode."""
        return self._current_theme
    
    @property
    def colors(self) -> dict:
        """Get current color scheme."""
        return self._colors.copy()
    
    @property
    def fonts(self) -> dict:
        """Get font configurations."""
        return self._fonts.copy()
    
    def set_theme(self, theme: str) -> None:
        """Switch to specified theme mode.
        
        Args:
            theme: Theme mode ('dark' or 'light')
            
        Raises:
            ValueError: If theme is not 'dark' or 'light'
        """
        if theme not in ('dark', 'light'):
            raise ValueError(f"Theme must be 'dark' or 'light', got '{theme}'")
        
        if theme == self._current_theme:
            return
        
        self._current_theme = theme
        self._colors = self.DARK_THEME if theme == 'dark' else self.LIGHT_THEME
        
        # Update CustomTkinter appearance
        ctk.set_appearance_mode(theme)
        
        # Notify all observers
        for observer in self._observers:
            try:
                observer(theme)
            except Exception as e:
                print(f"Error notifying theme observer: {e}")
    
    def get_color(self, key: str, default: Optional[str] = None) -> str:
        """Get specific color value.
        
        Args:
            key: Color key (e.g., 'bg_primary', 'accent_primary')
            default: Default value if key not found
            
        Returns:
            Color value as hex string
        """
        return self._colors.get(key, default or '#000000')
    
    def get_font(self, key: str, default: Optional[tuple] = None) -> tuple:
        """Get specific font configuration.
        
        Args:
            key: Font key (e.g., 'heading_large', 'body_medium')
            default: Default value if key not found
            
        Returns:
            Font tuple (family, size, weight)
        """
        return self._fonts.get(key, default or ('Segoe UI', 11, 'normal'))
    
    def add_observer(self, callback: Callable[[str], None]) -> None:
        """Add theme change observer.
        
        Args:
            callback: Function to call when theme changes,
                     receives new theme name as argument
        """
        if callback not in self._observers:
            self._observers.append(callback)
    
    def remove_observer(self, callback: Callable[[str], None]) -> None:
        """Remove theme change observer.
        
        Args:
            callback: Previously added callback function
        """
        if callback in self._observers:
            self._observers.remove(callback)


# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """Get global theme manager instance.
    
    Creates a new instance if one doesn't exist.
    
    Returns:
        Global ThemeManager instance
    """
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager(default_theme='dark')
    return _theme_manager


def set_theme_manager(manager: ThemeManager) -> None:
    """Set global theme manager instance.
    
    Args:
        manager: ThemeManager instance to use globally
    """
    global _theme_manager
    _theme_manager = manager