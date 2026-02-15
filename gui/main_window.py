"""Main window for PPT Translator GUI.

Provides the main application window with menu bar, toolbar, content area,
and status bar. Integrates all GUI components into a cohesive workflow.
"""

from typing import Optional, List
import customtkinter as ctk
from pathlib import Path

from .utils.theme_manager import get_theme_manager
from .utils.config_manager import get_config_manager
from .widgets.file_selector import FileSelector
from .widgets.provider_selector import ProviderSelector
from .widgets.progress_display import ProgressDisplay
from .dialogs.settings_dialog import SettingsDialog
from .dialogs.api_key_dialog import ApiKeyDialog

# Import core translation modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from ppt_translator.pipeline import process_ppt_file
from ppt_translator.translation import TranslationService
from ppt_translator.providers import create_provider


class MainWindow(ctk.CTk):
    """Main application window for PPT Translator.
    
    Provides the main application interface with menu bar, toolbar,
    content area for file selection, provider settings, progress display,
    and status bar.
    
    Attributes:
        selected_files: List of currently selected file paths
        is_translating: Whether translation is currently in progress
    
    Example:
        >>> app = MainWindow()
        >>> app.mainloop()
    """
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        self.theme_manager = get_theme_manager()
        self.config_manager = get_config_manager()
        
        # State variables
        self.selected_files: List[str] = []
        self.is_translating = False
        
        # Window configuration
        self._configure_window()
        
        # Create UI
        self._create_menu_bar()
        self._create_toolbar()
        self._create_content_area()
        self._create_status_bar()
        
        # Apply theme
        self._apply_theme()
        
        # Load window settings
        self._load_window_settings()
    
    def _configure_window(self) -> None:
        """Configure window properties."""
        self.title("PPT Translator")
        
        # Get saved window size or use defaults
        width = self.config_manager.get('window_width', 1200)
        height = self.config_manager.get('window_height', 800)
        
        self.geometry(f"{width}x{height}")
        self.minsize(900, 650)
        
        # Set icon if available
        try:
            self.iconbitmap("assets/icon.ico")
        except:
            pass  # Icon not available
        
        # Configure grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def _create_menu_bar(self) -> None:
        """Create menu bar."""
        # Note: CustomTkinter doesn't support native menu bars well
        # We'll create a custom menu frame instead
        
        self.menu_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.menu_frame.grid_propagate(False)
        
        # Menu buttons
        menus = [
            ("文件", self._show_file_menu),
            ("编辑", self._show_edit_menu),
            ("视图", self._show_view_menu),
            ("工具", self._show_tools_menu),
            ("帮助", self._show_help_menu),
        ]
        
        for text, command in menus:
            btn = ctk.CTkButton(
                self.menu_frame,
                text=text,
                command=command,
                width=60,
                height=20,
                corner_radius=0,
                fg_color="transparent",
                hover_color=self.theme_manager.get_color('bg_tertiary')
            )
            btn.pack(side='left', padx=2, pady=5)
    
    def _create_toolbar(self) -> None:
        """Create toolbar."""
        self.toolbar = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.toolbar.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.toolbar.grid_propagate(False)
        
        # Toolbar buttons
        toolbar_buttons = [
            ("打开", self._on_open_files, "打开 PPT 文件"),
            ("设置", self._on_open_settings, "打开设置"),
            ("开始", self._on_start_translation, "开始翻译"),
        ]
        
        for text, command, tooltip in toolbar_buttons:
            btn = ctk.CTkButton(
                self.toolbar,
                text=text,
                command=command,
                width=80,
                height=32
            )
            btn.pack(side='left', padx=5, pady=9)
            
            # Store tooltip for later implementation
            btn.tooltip = tooltip
    
    def _create_content_area(self) -> None:
        """Create main content area."""
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Create tabview for content sections
        self.content_tabs = ctk.CTkTabview(self.content_frame)
        self.content_tabs.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # File Selection Tab
        self.content_tabs.add("文件选择")
        self.file_selector = FileSelector(
            self.content_tabs.tab("文件选择"),
            on_selection_changed=self._on_files_selected
        )
        self.file_selector.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Provider Settings Tab
        self.content_tabs.add("翻译设置")
        self.provider_selector = ProviderSelector(
            self.content_tabs.tab("翻译设置"),
            on_config_changed=self._on_config_changed
        )
        self.provider_selector.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Progress Tab
        self.content_tabs.add("进度")
        self.progress_display = ProgressDisplay(
            self.content_tabs.tab("进度"),
            on_cancel=self._on_cancel_translation
        )
        self.progress_display.pack(fill='both', expand=True, padx=10, pady=10)
    
    def _create_status_bar(self) -> None:
        """Create status bar."""
        self.status_bar = ctk.CTkFrame(self, height=25, corner_radius=0)
        self.status_bar.grid(row=3, column=0, sticky="ew", padx=0, pady=0)
        self.status_bar.grid_propagate(False)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="就绪",
            font=self.theme_manager.get_font('body_small')
        )
        self.status_label.pack(side='left', padx=10, pady=2)
        
        # File count label
        self.file_count_label = ctk.CTkLabel(
            self.status_bar,
            text="0 个文件",
            font=self.theme_manager.get_font('body_small')
        )
        self.file_count_label.pack(side='right', padx=10, pady=2)
    
    def _apply_theme(self) -> None:
        """Apply theme colors to all widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_primary'])
        self.menu_frame.configure(fg_color=colors['bg_secondary'])
        self.toolbar.configure(fg_color=colors['bg_secondary'])
        self.content_frame.configure(fg_color=colors['bg_primary'])
        self.status_bar.configure(fg_color=colors['bg_tertiary'])
        
        # Update labels
        self.status_label.configure(text_color=colors['text_secondary'])
        self.file_count_label.configure(text_color=colors['text_secondary'])
    
    def _load_window_settings(self) -> None:
        """Load window position and size settings."""
        # Window position will be handled by window manager
        pass
    
    def _save_window_settings(self) -> None:
        """Save window position and size settings."""
        if not self.is_translating:  # Only save if not in middle of translation
            self.config_manager.set('window_width', self.winfo_width())
            self.config_manager.set('window_height', self.winfo_height())
            # Don't save maximized state for simplicity
            self.config_manager.save()
    
    # Event handlers
    def _on_files_selected(self, files: list) -> None:
        """Handle file selection."""
        self.selected_files = files
        self.file_count_label.configure(text=f"{len(files)} 个文件")
        self._set_status(f"已选择 {len(files)} 个文件")
    
    def _on_config_changed(self, config: dict) -> None:
        """Handle configuration changes."""
        # Configuration is auto-saved by the provider selector
        pass
    
    def _on_cancel_translation(self) -> None:
        """Handle translation cancellation."""
        self.is_translating = False
        self._set_status("翻译已取消")
        self.progress_display.stop_progress()
    
    # Menu handlers
    def _show_file_menu(self) -> None:
        """Show file menu."""
        # TODO: Implement context menu
        pass
    
    def _show_edit_menu(self) -> None:
        """Show edit menu."""
        pass
    
    def _show_view_menu(self) -> None:
        """Show view menu."""
        pass
    
    def _show_tools_menu(self) -> None:
        """Show tools menu."""
        pass
    
    def _show_help_menu(self) -> None:
        """Show help menu."""
        pass
    
    # Toolbar handlers
    def _on_open_files(self) -> None:
        """Handle open files button."""
        self._switch_to_tab("文件选择")
    
    def _on_open_settings(self) -> None:
        """Handle open settings button."""
        dialog = SettingsDialog(self)
        dialog.set_callback(self._on_settings_changed)
    
    def _on_start_translation(self) -> None:
        """Handle start translation button."""
        if not self.selected_files:
            self._show_error("请先选择要翻译的文件")
            return
        
        if self.is_translating:
            return
        
        # Switch to progress tab
        self._switch_to_tab("进度")
        
        # Start translation
        self._start_translation()
    
    # Translation logic
    def _start_translation(self) -> None:
        """Start the translation process."""
        self.is_translating = True
        self._set_status("正在翻译...")
        
        # Start progress display
        self.progress_display.start_progress()
        
        # Start translation in a separate thread
        import threading
        
        def run_translation():
            try:
                # Get translation configuration
                config = self.provider_selector.get_config()
                provider_name = config.get('provider', 'openai')
                api_key = config.get('api_key', '')
                model = config.get('model', '')
                source_lang = config.get('source_language', 'zh')
                target_lang = config.get('target_language', 'en')
                
                # Validate API key
                if not api_key:
                    self.progress_display.add_log("错误: 请先设置 API 密钥")
                    return
                
                # Create provider and translation service
                try:
                    # Set API key to environment variable for provider to read
                    import os
                    env_var_map = {
                        'openai': 'OPENAI_API_KEY',
                        'anthropic': 'ANTHROPIC_API_KEY',
                        'gemini': 'GOOGLE_API_KEY',
                        'deepseek': 'DEEPSEEK_API_KEY',
                        'grok': 'GROK_API_KEY',
                    }
                    env_var = env_var_map.get(provider_name, f'{provider_name.upper()}_API_KEY')
                    os.environ[env_var] = api_key
                    
                    from ppt_translator.providers.base import ProviderConfigurationError
                    provider = create_provider(provider_name, model=model)
                    translator = TranslationService(provider)
                except ProviderConfigurationError as e:
                    self.progress_display.add_log(f"错误: API 密钥配置错误 - {str(e)}")
                    return
                except Exception as e:
                    self.progress_display.add_log(f"错误: 无法创建翻译服务 - {str(e)}")
                    import traceback
                    self.progress_display.add_log(traceback.format_exc())
                    return
                
                total_files = len(self.selected_files)
                for i, file_path in enumerate(self.selected_files):
                    if not self.is_translating:
                        break
                    
                    self.progress_display.update_progress(
                        ((i) / total_files) * 100,
                        f"正在翻译: {Path(file_path).name}",
                        i,
                        total_files
                    )
                    
                    # Process the PPT file
                    try:
                        output_path = process_ppt_file(
                            Path(file_path),
                            translator=translator,
                            source_lang=source_lang,
                            target_lang=target_lang,
                            max_workers=4,
                            cleanup=True
                        )
                        
                        if output_path and output_path.exists():
                            self.progress_display.add_log(f"完成: {Path(file_path).name}")
                            self.progress_display.add_log(f"  输出: {output_path}")
                        else:
                            self.progress_display.add_log(f"失败: {Path(file_path).name} - 未生成输出文件")
                    except Exception as e:
                        self.progress_display.add_log(f"错误: {Path(file_path).name} - {str(e)}")
                        import traceback
                        self.progress_display.add_log(traceback.format_exc())
                    
                    self.progress_display.update_progress(
                        ((i + 1) / total_files) * 100,
                        f"完成: {Path(file_path).name}",
                        i + 1,
                        total_files
                    )
                
                if self.is_translating:
                    self.progress_display.update_progress(
                        100,
                        "翻译完成",
                        total_files,
                        total_files
                    )
                    self.progress_display.add_log("所有文件翻译完成")
                
            except Exception as e:
                self.progress_display.add_log(f"错误: {str(e)}")
                import traceback
                self.progress_display.add_log(traceback.format_exc())
            
            finally:
                self.progress_display.stop_progress()
                self.is_translating = False
                self._set_status("翻译完成")
        
        thread = threading.Thread(target=run_translation)
        thread.daemon = True
        thread.start()
    
    # Helper methods
    def _switch_to_tab(self, tab_name: str) -> None:
        """Switch to a specific tab."""
        try:
            self.content_tabs.set(tab_name)
        except:
            pass  # Tab doesn't exist
    
    def _set_status(self, message: str) -> None:
        """Set status bar message."""
        self.status_label.configure(text=message)
    
    def _show_error(self, message: str) -> None:
        """Show error message."""
        import tkinter.messagebox as messagebox
        messagebox.showerror("错误", message)
    
    def _on_settings_changed(self) -> None:
        """Handle settings changes."""
        # Reload theme if changed
        self._apply_theme()
        self._set_status("设置已更新")
    
    # Window event handlers
    def on_closing(self) -> None:
        """Handle window close event."""
        # Save window settings
        self._save_window_settings()
        
        # Stop any ongoing translation
        if self.is_translating:
            self.is_translating = False
        
        # Destroy window
        self.destroy()


def main():
    """Main entry point for the GUI application."""
    # Set theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Create and run main window
    app = MainWindow()
    
    # Set up close handler
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    app.mainloop()


if __name__ == '__main__':
    main()
