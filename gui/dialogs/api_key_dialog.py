"""API Key management dialog for PPT Translator GUI.

Provides a dialog for managing API keys for different translation providers.
"""

from typing import Optional, Callable
import customtkinter as ctk

from ..utils.theme_manager import get_theme_manager
from ..utils.config_manager import get_config_manager


class ApiKeyDialog(ctk.CTkToplevel):
    """API Key management dialog.
    
    Provides an interface for viewing, adding, editing, and testing API keys
    for different translation providers.
    
    Attributes:
        on_keys_changed: Callback when API keys are modified
    
    Example:
        >>> dialog = ApiKeyDialog(parent)
        >>> dialog.set_callback(on_keys_changed)
    """
    
    # Provider display names
    PROVIDER_NAMES = {
        'openai': 'OpenAI',
        'anthropic': 'Anthropic',
        'deepseek': 'DeepSeek',
        'grok': 'Grok',
        'gemini': 'Google Gemini',
    }
    
    def __init__(
        self,
        master,
        on_keys_changed: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """Initialize API key management dialog.
        
        Args:
            master: Parent widget
            on_keys_changed: Callback when API keys are modified
            **kwargs: Additional arguments passed to CTkToplevel
        """
        super().__init__(master, **kwargs)
        
        self.theme_manager = get_theme_manager()
        self.config_manager = get_config_manager()
        self.on_keys_changed = on_keys_changed
        
        # Dialog configuration
        self.title("API 密钥管理")
        self.geometry("700x500")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(master)
        self.grab_set()
        
        self._create_widgets()
        self._apply_theme()
        self._load_keys()
        
        # Center the dialog
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="API 密钥管理",
            font=self.theme_manager.get_font('heading_medium')
        )
        self.title_label.pack(pady=(20, 10))
        
        # Description
        self.desc_label = ctk.CTkLabel(
            self,
            text="管理各翻译服务的 API 密钥。密钥将被安全加密存储。",
            font=self.theme_manager.get_font('body_small'),
            wraplength=600
        )
        self.desc_label.pack(pady=(0, 20))
        
        # Keys table frame
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Table headers
        self.header_frame = ctk.CTkFrame(self.table_frame, fg_color='transparent')
        self.header_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            self.header_frame,
            text="提供商",
            font=self.theme_manager.get_font('body_medium'),
            width=120
        ).pack(side='left', padx=(0, 10))
        
        ctk.CTkLabel(
            self.header_frame,
            text="API 密钥",
            font=self.theme_manager.get_font('body_medium'),
            width=250
        ).pack(side='left', padx=(0, 10))
        
        ctk.CTkLabel(
            self.header_frame,
            text="状态",
            font=self.theme_manager.get_font('body_medium'),
            width=80
        ).pack(side='left', padx=(0, 10))
        
        ctk.CTkLabel(
            self.header_frame,
            text="操作",
            font=self.theme_manager.get_font('body_medium'),
            width=60
        ).pack(side='left')
        
        # Scrollable frame for key rows
        self.keys_scroll_frame = ctk.CTkScrollableFrame(
            self.table_frame,
            height=200
        )
        self.keys_scroll_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Test all button
        self.test_all_btn = ctk.CTkButton(
            self,
            text="测试所有密钥",
            command=self._test_all_keys,
            width=150
        )
        self.test_all_btn.pack(pady=10)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="关闭",
            command=self.destroy,
            width=100
        )
        self.cancel_btn.pack(side='right')
    
    def _apply_theme(self) -> None:
        """Apply current theme colors to widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_primary'])
        self.table_frame.configure(fg_color=colors['bg_secondary'])
        self.keys_scroll_frame.configure(fg_color=colors['bg_tertiary'])
    
    def _load_keys(self) -> None:
        """Load API keys from config manager."""
        # Clear existing rows
        for widget in self.keys_scroll_frame.winfo_children():
            widget.destroy()
        
        # Load keys for each provider
        providers = ['openai', 'anthropic', 'deepseek', 'grok', 'gemini']
        
        for provider in providers:
            self._create_key_row(provider)
    
    def _create_key_row(self, provider: str) -> None:
        """Create a key row for a provider.
        
        Args:
            provider: Provider key name
        """
        provider_config = self.config_manager.get_provider_config(provider)
        has_key = bool(provider_config.api_key)
        
        # Row frame
        row_frame = ctk.CTkFrame(self.keys_scroll_frame, fg_color='transparent')
        row_frame.pack(fill='x', pady=2)
        
        # Provider name
        provider_label = ctk.CTkLabel(
            row_frame,
            text=self.PROVIDER_NAMES.get(provider, provider),
            font=self.theme_manager.get_font('body_medium'),
            width=120
        )
        provider_label.pack(side='left', padx=(0, 10))
        
        # API key (masked)
        key_text = "●●●●●●●●" if has_key else "(未设置)"
        key_label = ctk.CTkLabel(
            row_frame,
            text=key_text,
            font=self.theme_manager.get_font('monospace'),
            width=250
        )
        key_label.pack(side='left', padx=(0, 10))
        
        # Status
        status_text = "已配置" if has_key else "未配置"
        status_color = self.theme_manager.get_color('success') if has_key else self.theme_manager.get_color('text_disabled')
        status_label = ctk.CTkLabel(
            row_frame,
            text=status_text,
            font=self.theme_manager.get_font('body_small'),
            text_color=status_color,
            width=80
        )
        status_label.pack(side='left', padx=(0, 10))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            row_frame,
            text="编辑",
            command=lambda p=provider: self._edit_key(p),
            width=60
        )
        edit_btn.pack(side='left')
    
    def _edit_key(self, provider: str) -> None:
        """Open dialog to edit API key for a provider.
        
        Args:
            provider: Provider key name
        """
        dialog = _EditKeyDialog(self, provider)
        dialog.grab_set()
        self.wait_window(dialog)
        
        # Reload keys
        self._load_keys()
    
    def _test_all_keys(self) -> None:
        """Test all configured API keys."""
        import tkinter.messagebox as messagebox
        
        # TODO: Implement actual API key testing
        messagebox.showinfo(
            "测试 API 密钥",
            "API 密钥测试功能将在后续版本中实现。"
        )
    
    def set_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for settings changes.
        
        Args:
            callback: Function to call when settings are changed
        """
        self.on_settings_changed = callback


class _EditKeyDialog(ctk.CTkToplevel):
    """Dialog for editing a single API key."""
    
    def __init__(self, master, provider: str, **kwargs):
        super().__init__(master, **kwargs)
        
        self.theme_manager = get_theme_manager()
        self.config_manager = get_config_manager()
        self.provider = provider
        
        # Dialog configuration
        self.title(f"编辑 {provider} API 密钥")
        self.geometry("450x200")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(master)
        self.grab_set()
        
        self._create_widgets()
        self._apply_theme()
        self._load_key()
        
        # Center the dialog
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Provider label
        self.provider_label = ctk.CTkLabel(
            self,
            text=f"提供商: {self.provider}",
            font=self.theme_manager.get_font('body_medium')
        )
        self.provider_label.pack(pady=(20, 10))
        
        # API Key entry
        self.key_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.key_frame.pack(fill='x', padx=20, pady=10)
        
        ctk.CTkLabel(
            self.key_frame,
            text="API 密钥:",
            font=self.theme_manager.get_font('body_medium')
        ).pack(side='left', padx=(0, 10))
        
        self.key_var = ctk.StringVar()
        self.key_entry = ctk.CTkEntry(
            self.key_frame,
            textvariable=self.key_var,
            show="●",
            width=250
        )
        self.key_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.show_btn = ctk.CTkButton(
            self.key_frame,
            text="显示",
            command=self._toggle_visibility,
            width=60
        )
        self.show_btn.pack(side='left')
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.button_frame.pack(fill='x', padx=20, pady=20)
        
        # Delete button
        self.delete_btn = ctk.CTkButton(
            self.button_frame,
            text="删除",
            command=self._delete_key,
            fg_color=self.theme_manager.get_color('error'),
            hover_color=self.theme_manager.get_color('error'),
            width=80
        )
        self.delete_btn.pack(side='left')
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="取消",
            command=self.destroy,
            width=80
        )
        self.cancel_btn.pack(side='right')
        
        # Save button
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="保存",
            command=self._save_key,
            width=80
        )
        self.save_btn.pack(side='right', padx=(0, 10))
    
    def _apply_theme(self) -> None:
        """Apply current theme colors to widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_primary'])
        self.button_frame.configure(fg_color='transparent')
    
    def _load_key(self) -> None:
        """Load existing API key."""
        provider_config = self.config_manager.get_provider_config(self.provider)
        if provider_config.api_key:
            self.key_var.set(provider_config.api_key)
    
    def _toggle_visibility(self) -> None:
        """Toggle API key visibility."""
        current_show = self.key_entry.cget('show')
        if current_show == '●':
            self.key_entry.configure(show='')
            self.show_btn.configure(text='隐藏')
        else:
            self.key_entry.configure(show='●')
            self.show_btn.configure(text='显示')
    
    def _save_key(self) -> None:
        """Save the API key."""
        key = self.key_var.get().strip()
        
        if not key:
            import tkinter.messagebox as messagebox
            result = messagebox.askyesno(
                "确认",
                "API 密钥为空，确定要删除此密钥吗？"
            )
            if not result:
                return
        
        # Save to config
        provider_config = self.config_manager.get_provider_config(self.provider)
        provider_config.api_key = key
        provider_config.enabled = bool(key)
        self.config_manager.set_provider_config(self.provider, provider_config)
        self.config_manager.save()
        
        self.destroy()
    
    def _delete_key(self) -> None:
        """Delete the API key."""
        import tkinter.messagebox as messagebox
        
        result = messagebox.askyesno(
            "确认",
            f"确定要删除 {self.provider} 的 API 密钥吗？"
        )
        
        if result:
            # Delete from config
            provider_config = self.config_manager.get_provider_config(self.provider)
            provider_config.api_key = ''
            provider_config.enabled = False
            self.config_manager.set_provider_config(self.provider, provider_config)
            self.config_manager.save()
            
            self.destroy()


def main():
    """Test the API key management dialog."""
    import customtkinter as ctk
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    app = ctk.CTk()
    app.title("Test Window")
    app.geometry("800x600")
    
    def open_dialog():
        dialog = ApiKeyDialog(app)
        dialog.set_callback(lambda: print("Keys changed!"))
    
    btn = ctk.CTkButton(app, text="管理 API 密钥", command=open_dialog)
    btn.pack(pady=50)
    
    app.mainloop()


if __name__ == '__main__':
    main()
