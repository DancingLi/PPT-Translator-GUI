"""About dialog for PPT Translator GUI.

Provides a dialog displaying application information, version details,
copyright, acknowledgments, and links to project resources.
"""

from typing import Optional, Callable
import customtkinter as ctk
import webbrowser

from ..utils.theme_manager import get_theme_manager


class AboutDialog(ctk.CTkToplevel):
    """About dialog for displaying application information.
    
    Shows application icon, name, version, build date, copyright,
    acknowledgments list, check update button, and project homepage link.
    
    Attributes:
        on_check_update: Callback when check update button is clicked
    
    Example:
        >>> dialog = AboutDialog(parent)
        >>> dialog.set_callback(on_check_update)
    """
    
    # Application information
    APP_NAME = "PPT Translator"
    APP_VERSION = "1.0.0"
    BUILD_DATE = "2026-02-15"
    COPYRIGHT = "© 2026 PPT Translator Team. All rights reserved."
    LICENSE = "MIT License"
    HOMEPAGE = "https://github.com/yourusername/ppt-translator"
    
    # Third-party acknowledgments
    ACKNOWLEDGMENTS = [
        ("customtkinter", "Modern looking GUI for Python"),
        ("python-pptx", "Python library for creating and modifying PowerPoint files"),
        ("openai", "OpenAI Python client library"),
        ("anthropic", "Anthropic Python client library"),
        ("google-generativeai", "Google Generative AI Python client"),
        ("Pillow", "Python Imaging Library"),
        ("pytest", "Python testing framework"),
    ]
    
    def __init__(
        self,
        master,
        on_check_update: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """Initialize about dialog.
        
        Args:
            master: Parent widget
            on_check_update: Callback when check update button is clicked
            **kwargs: Additional arguments passed to CTkToplevel
        """
        super().__init__(master, **kwargs)
        
        self.theme_manager = get_theme_manager()
        self.on_check_update = on_check_update
        
        # Dialog configuration
        self.title("关于")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(master)
        self.grab_set()
        
        self._create_widgets()
        self._apply_theme()
        
        # Center the dialog
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Main scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # App icon (placeholder)
        self.icon_label = ctk.CTkLabel(
            self.scroll_frame,
            text="📄",
            font=('Segoe UI', 64)
        )
        self.icon_label.pack(pady=(0, 10))
        
        # App name
        self.name_label = ctk.CTkLabel(
            self.scroll_frame,
            text=self.APP_NAME,
            font=self.theme_manager.get_font('heading_large')
        )
        self.name_label.pack()
        
        # Version
        self.version_label = ctk.CTkLabel(
            self.scroll_frame,
            text=f"版本 {self.APP_VERSION}",
            font=self.theme_manager.get_font('body_medium'),
            text_color=self.theme_manager.get_color('text_secondary')
        )
        self.version_label.pack()
        
        # Build date
        self.build_label = ctk.CTkLabel(
            self.scroll_frame,
            text=f"构建日期: {self.BUILD_DATE}",
            font=self.theme_manager.get_font('body_small'),
            text_color=self.theme_manager.get_color('text_secondary')
        )
        self.build_label.pack(pady=(0, 20))
        
        # Copyright
        self.copyright_label = ctk.CTkLabel(
            self.scroll_frame,
            text=self.COPYRIGHT,
            font=self.theme_manager.get_font('body_small')
        )
        self.copyright_label.pack()
        
        # License
        self.license_label = ctk.CTkLabel(
            self.scroll_frame,
            text=f"许可: {self.LICENSE}",
            font=self.theme_manager.get_font('body_small'),
            text_color=self.theme_manager.get_color('text_secondary')
        )
        self.license_label.pack(pady=(0, 20))
        
        # Homepage link
        self.homepage_btn = ctk.CTkButton(
            self.scroll_frame,
            text="访问项目主页",
            command=self._open_homepage,
            width=150
        )
        self.homepage_btn.pack(pady=(0, 20))
        
        # Check update button
        self.update_btn = ctk.CTkButton(
            self.scroll_frame,
            text="检查更新",
            command=self._check_update,
            width=150
        )
        self.update_btn.pack(pady=(0, 20))
        
        # Acknowledgments section
        self.ack_frame = ctk.CTkFrame(self.scroll_frame)
        self.ack_frame.pack(fill='x', pady=20)
        
        self.ack_label = ctk.CTkLabel(
            self.ack_frame,
            text="致谢",
            font=self.theme_manager.get_font('heading_small')
        )
        self.ack_label.pack(pady=10)
        
        # Acknowledgments list
        for name, description in self.ACKNOWLEDGMENTS:
            ack_item = ctk.CTkLabel(
                self.ack_frame,
                text=f"• {name}: {description}",
                font=self.theme_manager.get_font('body_small'),
                wraplength=400
            )
            ack_item.pack(anchor='w', padx=20, pady=2)
        
        # Close button
        self.close_btn = ctk.CTkButton(
            self,
            text="关闭",
            command=self.destroy,
            width=100
        )
        self.close_btn.pack(pady=20)
    
    def _apply_theme(self) -> None:
        """Apply current theme colors to widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_primary'])
        self.scroll_frame.configure(fg_color=colors['bg_primary'])
        self.ack_frame.configure(fg_color=colors['bg_secondary'])
    
    def _open_homepage(self) -> None:
        """Open project homepage in browser."""
        try:
            webbrowser.open(self.HOMEPAGE)
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("错误", f"无法打开主页: {e}")
    
    def _check_update(self) -> None:
        """Check for application updates."""
        if self.on_check_update:
            self.on_check_update()
        else:
            import tkinter.messagebox as messagebox
            messagebox.showinfo(
                "检查更新",
                "当前已是最新版本。\n\n版本: {}\n构建日期: {}".format(
                    self.APP_VERSION,
                    self.BUILD_DATE
                )
            )
    
    def set_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for check update button.
        
        Args:
            callback: Function to call when check update button is clicked
        """
        self.on_check_update = callback


def main():
    """Test the about dialog."""
    import customtkinter as ctk
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = ctk.CTk()
    app.title("Test Window")
    app.geometry("800x600")
    
    def open_dialog():
        dialog = AboutDialog(app)
        dialog.set_callback(lambda: print("Check update clicked!"))
    
    btn = ctk.CTkButton(app, text="关于", command=open_dialog)
    btn.pack(pady=50)
    
    app.mainloop()


if __name__ == '__main__':
    main()
