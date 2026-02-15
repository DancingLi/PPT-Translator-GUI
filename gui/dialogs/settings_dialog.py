"""Settings dialog for PPT Translator GUI.

Provides a dialog for configuring application settings including general,
translation, and advanced options.
"""

from typing import Optional, Callable
import customtkinter as ctk

from ..utils.theme_manager import get_theme_manager
from ..utils.config_manager import get_config_manager


class SettingsDialog(ctk.CTkToplevel):
    """Settings dialog for application configuration.
    
    Provides tabs for general, translation, and advanced settings with
    options to apply, reset, or cancel changes.
    
    Attributes:
        on_settings_changed: Callback when settings are applied
    
    Example:
        >>> dialog = SettingsDialog(parent)
        >>> dialog.set_callback(on_settings_changed)
    """
    
    def __init__(
        self,
        master,
        on_settings_changed: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """Initialize settings dialog.
        
        Args:
            master: Parent widget
            on_settings_changed: Callback when settings are applied
            **kwargs: Additional arguments passed to CTkToplevel
        """
        super().__init__(master, **kwargs)
        
        self.theme_manager = get_theme_manager()
        self.config_manager = get_config_manager()
        self.on_settings_changed = on_settings_changed
        
        # Dialog configuration
        self.title("设置")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(master)
        self.grab_set()
        
        self._create_widgets()
        self._apply_theme()
        self._load_settings()
        
        # Center the dialog
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Tabview for settings categories
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill='both', expand=True, padx=20, pady=20)
        
        # General settings tab
        self.tabview.add("常规")
        self._create_general_tab()
        
        # Translation settings tab
        self.tabview.add("翻译")
        self._create_translation_tab()
        
        # Advanced settings tab
        self.tabview.add("高级")
        self._create_advanced_tab()
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Reset to defaults button
        self.reset_btn = ctk.CTkButton(
            self.button_frame,
            text="恢复默认",
            command=self._reset_to_defaults,
            width=100
        )
        self.reset_btn.pack(side='left')
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="取消",
            command=self.destroy,
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        # Apply button
        self.apply_btn = ctk.CTkButton(
            self.button_frame,
            text="应用",
            command=self._apply_settings,
            width=100
        )
        self.apply_btn.pack(side='right')
    
    def _create_general_tab(self) -> None:
        """Create general settings tab."""
        tab = self.tabview.tab("常规")
        
        # Theme selection
        theme_frame = ctk.CTkFrame(tab, fg_color='transparent')
        theme_frame.pack(fill='x', padx=10, pady=(20, 10))
        
        ctk.CTkLabel(
            theme_frame,
            text="主题:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.theme_var = ctk.StringVar(value='dark')
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=['dark', 'light'],
            variable=self.theme_var,
            width=120
        )
        self.theme_menu.pack(side='left')
        
        # Language selection
        lang_frame = ctk.CTkFrame(tab, fg_color='transparent')
        lang_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            lang_frame,
            text="界面语言:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.ui_lang_var = ctk.StringVar(value='zh')
        self.ui_lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=['zh', 'en'],
            variable=self.ui_lang_var,
            width=120
        )
        self.ui_lang_menu.pack(side='left')
        
        # Auto update checkbox
        self.auto_update_var = ctk.BooleanVar(value=True)
        self.auto_update_checkbox = ctk.CTkCheckBox(
            tab,
            text="自动检查更新",
            variable=self.auto_update_var,
            font=self.theme_manager.get_font('body_medium')
        )
        self.auto_update_checkbox.pack(anchor='w', padx=10, pady=20)
    
    def _create_translation_tab(self) -> None:
        """Create translation settings tab."""
        tab = self.tabview.tab("翻译")
        
        # Default provider
        provider_frame = ctk.CTkFrame(tab, fg_color='transparent')
        provider_frame.pack(fill='x', padx=10, pady=(20, 10))
        
        ctk.CTkLabel(
            provider_frame,
            text="默认提供商:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.default_provider_var = ctk.StringVar(value='openai')
        self.default_provider_menu = ctk.CTkOptionMenu(
            provider_frame,
            values=['openai', 'anthropic', 'deepseek', 'grok', 'gemini'],
            variable=self.default_provider_var,
            width=150
        )
        self.default_provider_menu.pack(side='left')
        
        # Default source language
        source_lang_frame = ctk.CTkFrame(tab, fg_color='transparent')
        source_lang_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            source_lang_frame,
            text="默认源语言:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.default_source_lang_var = ctk.StringVar(value='zh')
        self.default_source_lang_menu = ctk.CTkOptionMenu(
            source_lang_frame,
            values=['zh', 'en', 'ja', 'ko', 'fr', 'de', 'es'],
            variable=self.default_source_lang_var,
            width=120
        )
        self.default_source_lang_menu.pack(side='left')
        
        # Default target language
        target_lang_frame = ctk.CTkFrame(tab, fg_color='transparent')
        target_lang_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            target_lang_frame,
            text="默认目标语言:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.default_target_lang_var = ctk.StringVar(value='en')
        self.default_target_lang_menu = ctk.CTkOptionMenu(
            target_lang_frame,
            values=['zh', 'en', 'ja', 'ko', 'fr', 'de', 'es'],
            variable=self.default_target_lang_var,
            width=120
        )
        self.default_target_lang_menu.pack(side='left')
    
    def _create_advanced_tab(self) -> None:
        """Create advanced settings tab."""
        tab = self.tabview.tab("高级")
        
        # Max workers
        workers_frame = ctk.CTkFrame(tab, fg_color='transparent')
        workers_frame.pack(fill='x', padx=10, pady=(20, 10))
        
        ctk.CTkLabel(
            workers_frame,
            text="最大线程数:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.max_workers_var = ctk.StringVar(value='4')
        self.max_workers_entry = ctk.CTkEntry(
            workers_frame,
            textvariable=self.max_workers_var,
            width=80
        )
        self.max_workers_entry.pack(side='left')
        
        # Max chunk size
        chunk_frame = ctk.CTkFrame(tab, fg_color='transparent')
        chunk_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            chunk_frame,
            text="分块大小 (字符):",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.chunk_size_var = ctk.StringVar(value='1000')
        self.chunk_size_entry = ctk.CTkEntry(
            chunk_frame,
            textvariable=self.chunk_size_var,
            width=80
        )
        self.chunk_size_entry.pack(side='left')
        
        # Output directory
        output_frame = ctk.CTkFrame(tab, fg_color='transparent')
        output_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(
            output_frame,
            text="输出目录:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.output_dir_var = ctk.StringVar()
        self.output_dir_entry = ctk.CTkEntry(
            output_frame,
            textvariable=self.output_dir_var,
            width=250
        )
        self.output_dir_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.browse_btn = ctk.CTkButton(
            output_frame,
            text="浏览",
            command=self._browse_output_dir,
            width=60
        )
        self.browse_btn.pack(side='left')
        
        # Keep intermediate files
        self.keep_intermediate_var = ctk.BooleanVar(value=False)
        self.keep_intermediate_checkbox = ctk.CTkCheckBox(
            tab,
            text="保留中间文件",
            variable=self.keep_intermediate_var,
            font=self.theme_manager.get_font('body_medium')
        )
        self.keep_intermediate_checkbox.pack(anchor='w', padx=10, pady=20)
    
    def _browse_output_dir(self) -> None:
        """Browse for output directory."""
        import tkinter.filedialog as filedialog
        
        directory = filedialog.askdirectory(
            title="选择输出目录"
        )
        
        if directory:
            self.output_dir_var.set(directory)
    
    def _apply_theme(self) -> None:
        """Apply current theme colors to widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_primary'])
        self.tabview.configure(
            fg_color=colors['bg_secondary'],
            segmented_button_selected_color=colors['accent_primary'],
            segmented_button_selected_hover_color=colors['accent_hover']
        )
        self.button_frame.configure(fg_color='transparent')
    
    def _load_settings(self) -> None:
        """Load settings from config manager."""
        # General settings
        self.theme_var.set(self.config_manager.get('theme', 'dark'))
        self.ui_lang_var.set(self.config_manager.get('language', 'zh'))
        self.auto_update_var.set(self.config_manager.get('auto_update', True))
        
        # Translation settings
        self.default_provider_var.set(self.config_manager.get('default_provider', 'openai'))
        self.default_source_lang_var.set(self.config_manager.get('source_language', 'zh'))
        self.default_target_lang_var.set(self.config_manager.get('target_language', 'en'))
        
        # Advanced settings
        self.max_workers_var.set(str(self.config_manager.get('max_workers', 4)))
        self.chunk_size_var.set(str(self.config_manager.get('max_chunk_size', 1000)))
        self.output_dir_var.set(self.config_manager.get('output_directory', ''))
        self.keep_intermediate_var.set(self.config_manager.get('keep_intermediate', False))
    
    def _apply_settings(self) -> None:
        """Apply settings to config manager."""
        try:
            # General settings
            self.config_manager.set('theme', self.theme_var.get())
            self.config_manager.set('language', self.ui_lang_var.get())
            self.config_manager.set('auto_update', self.auto_update_var.get())
            
            # Translation settings
            self.config_manager.set('default_provider', self.default_provider_var.get())
            self.config_manager.set('source_language', self.default_source_lang_var.get())
            self.config_manager.set('target_language', self.default_target_lang_var.get())
            
            # Advanced settings
            self.config_manager.set('max_workers', int(self.max_workers_var.get()))
            self.config_manager.set('max_chunk_size', int(self.chunk_size_var.get()))
            self.config_manager.set('output_directory', self.output_dir_var.get())
            self.config_manager.set('keep_intermediate', self.keep_intermediate_var.get())
            
            # Save to file
            self.config_manager.save()
            
            # Notify callback
            if self.on_settings_changed:
                self.on_settings_changed()
            
            # Close dialog
            self.destroy()
            
        except ValueError as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("错误", f"设置值无效: {e}")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("错误", f"保存设置失败: {e}")
    
    def _reset_to_defaults(self) -> None:
        """Reset settings to default values."""
        import tkinter.messagebox as messagebox
        
        result = messagebox.askyesno(
            "确认",
            "确定要恢复默认设置吗？\n所有自定义设置将被重置。"
        )
        
        if result:
            # Reset to defaults
            self.theme_var.set('dark')
            self.ui_lang_var.set('zh')
            self.auto_update_var.set(True)
            
            self.default_provider_var.set('openai')
            self.default_source_lang_var.set('zh')
            self.default_target_lang_var.set('en')
            
            self.max_workers_var.set('4')
            self.chunk_size_var.set('1000')
            self.output_dir_var.set('')
            self.keep_intermediate_var.set(False)


# Alias for backwards compatibility
SettingsDialog = SettingsDialog


def main():
    """Test the settings dialog."""
    import customtkinter as ctk
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = ctk.CTk()
    app.title("Test Window")
    app.geometry("800x600")
    
    def open_settings():
        dialog = SettingsDialog(app)
        dialog.set_callback(lambda: print("Settings changed!"))
    
    btn = ctk.CTkButton(app, text="打开设置", command=open_settings)
    btn.pack(pady=50)
    
    app.mainloop()


if __name__ == '__main__':
    main()
