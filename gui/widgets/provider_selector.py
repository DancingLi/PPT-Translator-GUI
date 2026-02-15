"""Provider selector component for PPT Translator GUI.

Provides a reusable component for selecting translation providers,
configuring API keys, and selecting source/target languages.
"""

from typing import Dict, List, Callable, Optional
import customtkinter as ctk

from ..utils.theme_manager import get_theme_manager
from ..utils.config_manager import get_config_manager


# Provider definitions
PROVIDERS = {
    'openai': {
        'name': 'OpenAI',
        'description': 'GPT-4, GPT-3.5 系列模型',
        'default_model': 'gpt-4o',
        'models': ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        'requires_api_key': True,
    },
    'anthropic': {
        'name': 'Anthropic',
        'description': 'Claude 系列模型',
        'default_model': 'claude-3-opus-20240229',
        'models': [
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307'
        ],
        'requires_api_key': True,
    },
    'deepseek': {
        'name': 'DeepSeek',
        'description': 'DeepSeek Chat 模型',
        'default_model': 'deepseek-chat',
        'models': ['deepseek-chat', 'deepseek-coder'],
        'requires_api_key': True,
    },
    'grok': {
        'name': 'Grok',
        'description': 'Grok 模型 (xAI)',
        'default_model': 'grok-1',
        'models': ['grok-1', 'grok-1.5'],
        'requires_api_key': True,
    },
    'gemini': {
        'name': 'Google Gemini',
        'description': 'Gemini 系列模型',
        'default_model': 'gemini-1.5-pro',
        'models': ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-pro'],
        'requires_api_key': True,
    },
}

# Language definitions
LANGUAGES = {
    'zh': '中文 (简体)',
    'zh-tw': '中文 (繁体)',
    'en': 'English',
    'ja': '日本語',
    'ko': '한국어',
    'fr': 'Français',
    'de': 'Deutsch',
    'es': 'Español',
    'it': 'Italiano',
    'pt': 'Português',
    'ru': 'Русский',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'th': 'ไทย',
    'vi': 'Tiếng Việt',
}


class ProviderSelector(ctk.CTkFrame):
    """Provider selector component for translation configuration.
    
    Provides a complete interface for selecting translation providers,
    configuring API keys, selecting models, and choosing source/target languages.
    
    Attributes:
        current_provider: Currently selected provider key
        on_config_changed: Callback when configuration changes
    
    Example:
        >>> selector = ProviderSelector(parent)
        >>> selector.pack(fill='both', expand=True)
        >>> selector.set_callback(on_config_changed)
    """
    
    def __init__(
        self,
        master,
        on_config_changed: Optional[Callable[[Dict], None]] = None,
        **kwargs
    ):
        """Initialize provider selector component.
        
        Args:
            master: Parent widget
            on_config_changed: Callback function when configuration changes
            **kwargs: Additional arguments passed to CTkFrame
        """
        super().__init__(master, **kwargs)
        
        self.theme_manager = get_theme_manager()
        self.config_manager = get_config_manager()
        self.on_config_changed = on_config_changed
        
        self.current_provider: str = self.config_manager.get('default_provider', 'openai')
        
        self._create_widgets()
        self._apply_theme()
        self._load_config()
    
    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="翻译设置",
            font=self.theme_manager.get_font('heading_small')
        )
        self.title_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Provider selection
        self.provider_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.provider_frame.pack(fill='x', padx=10, pady=5)
        
        self.provider_label = ctk.CTkLabel(
            self.provider_frame,
            text="翻译提供商:",
            font=self.theme_manager.get_font('body_medium')
        )
        self.provider_label.pack(side='left', padx=(0, 10))
        
        self.provider_var = ctk.StringVar(value=self.current_provider)
        self.provider_menu = ctk.CTkOptionMenu(
            self.provider_frame,
            values=list(PROVIDERS.keys()),
            variable=self.provider_var,
            command=self._on_provider_changed,
            width=150
        )
        self.provider_menu.pack(side='left')
        
        # Provider info
        self.provider_info = ctk.CTkLabel(
            self,
            text="",
            font=self.theme_manager.get_font('body_small'),
            wraplength=500
        )
        self.provider_info.pack(anchor='w', padx=10, pady=(0, 5))
        
        # API Key
        self.api_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.api_frame.pack(fill='x', padx=10, pady=5)
        
        self.api_label = ctk.CTkLabel(
            self.api_frame,
            text="API 密钥:",
            font=self.theme_manager.get_font('body_medium')
        )
        self.api_label.pack(side='left', padx=(0, 10))
        
        self.api_key_var = ctk.StringVar()
        self.api_key_entry = ctk.CTkEntry(
            self.api_frame,
            textvariable=self.api_key_var,
            show="●",
            width=250
        )
        self.api_key_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.show_key_btn = ctk.CTkButton(
            self.api_frame,
            text="显示",
            width=60,
            command=self._toggle_key_visibility
        )
        self.show_key_btn.pack(side='left', padx=(0, 5))
        
        self.verify_btn = ctk.CTkButton(
            self.api_frame,
            text="验证",
            width=60,
            command=self._verify_api_key
        )
        self.verify_btn.pack(side='left')
        
        # Model selection
        self.model_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.model_frame.pack(fill='x', padx=10, pady=5)
        
        self.model_label = ctk.CTkLabel(
            self.model_frame,
            text="模型:",
            font=self.theme_manager.get_font('body_medium')
        )
        self.model_label.pack(side='left', padx=(0, 10))
        
        self.model_var = ctk.StringVar()
        self.model_menu = ctk.CTkOptionMenu(
            self.model_frame,
            values=[],
            variable=self.model_var,
            width=200
        )
        self.model_menu.pack(side='left')
        
        # Language selection
        self.lang_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.lang_frame.pack(fill='x', padx=10, pady=5)
        
        # Source language
        self.source_lang_label = ctk.CTkLabel(
            self.lang_frame,
            text="源语言:",
            font=self.theme_manager.get_font('body_medium')
        )
        self.source_lang_label.pack(side='left', padx=(0, 5))
        
        self.source_lang_var = ctk.StringVar(value='zh')
        self.source_lang_menu = ctk.CTkOptionMenu(
            self.lang_frame,
            values=list(LANGUAGES.keys()),
            variable=self.source_lang_var,
            command=self._update_language_labels,
            width=120
        )
        self.source_lang_menu.pack(side='left', padx=(0, 20))
        
        # Target language
        self.target_lang_label = ctk.CTkLabel(
            self.lang_frame,
            text="目标语言:",
            font=self.theme_manager.get_font('body_medium')
        )
        self.target_lang_label.pack(side='left', padx=(0, 5))
        
        self.target_lang_var = ctk.StringVar(value='en')
        self.target_lang_menu = ctk.CTkOptionMenu(
            self.lang_frame,
            values=list(LANGUAGES.keys()),
            variable=self.target_lang_var,
            command=self._update_language_labels,
            width=120
        )
        self.target_lang_menu.pack(side='left')
        
        # Language display labels
        self.lang_display_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.lang_display_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.source_lang_display = ctk.CTkLabel(
            self.lang_display_frame,
            text="中文 (简体)",
            font=self.theme_manager.get_font('body_small'),
            text_color=self.theme_manager.get_color('text_secondary')
        )
        self.source_lang_display.pack(side='left', padx=(70, 0))
        
        self.arrow_label = ctk.CTkLabel(
            self.lang_display_frame,
            text="→",
            font=self.theme_manager.get_font('body_medium')
        )
        self.arrow_label.pack(side='left', padx=20)
        
        self.target_lang_display = ctk.CTkLabel(
            self.lang_display_frame,
            text="English",
            font=self.theme_manager.get_font('body_small'),
            text_color=self.theme_manager.get_color('text_secondary')
        )
        self.target_lang_display.pack(side='left')
    
    def _update_language_labels(self, *args) -> None:
        """Update language display labels."""
        source_lang = self.source_lang_var.get()
        target_lang = self.target_lang_var.get()
        
        self.source_lang_display.configure(text=LANGUAGES.get(source_lang, source_lang))
        self.target_lang_display.configure(text=LANGUAGES.get(target_lang, target_lang))
        
        # Notify callback
        if self.on_config_changed:
            self.on_config_changed(self.get_config())
    
    def _on_provider_changed(self, provider: str) -> None:
        """Handle provider selection change."""
        self.current_provider = provider
        
        # Update provider info
        provider_info = PROVIDERS.get(provider, {})
        self.provider_info.configure(
            text=f"{provider_info.get('name', provider)} - {provider_info.get('description', '')}"
        )
        
        # Update model dropdown
        models = provider_info.get('models', [])
        self.model_menu.configure(values=models)
        if models:
            self.model_var.set(models[0])
        
        # Load saved config for this provider
        self._load_provider_config(provider)
        
        # Notify callback
        if self.on_config_changed:
            self.on_config_changed(self.get_config())
    
    def _toggle_key_visibility(self) -> None:
        """Toggle API key visibility."""
        current_show = self.api_key_entry.cget('show')
        if current_show == '●':
            self.api_key_entry.configure(show='')
            self.show_key_btn.configure(text='隐藏')
        else:
            self.api_key_entry.configure(show='●')
            self.show_key_btn.configure(text='显示')
    
    def _verify_api_key(self) -> None:
        """Verify the API key."""
        # TODO: Implement actual API verification
        import tkinter.messagebox as messagebox
        messagebox.showinfo("验证", "API 密钥验证功能待实现")
    
    def _load_config(self) -> None:
        """Load configuration from config manager."""
        # Load default provider
        default_provider = self.config_manager.get('default_provider', 'openai')
        self.provider_var.set(default_provider)
        self._on_provider_changed(default_provider)
        
        # Load language settings
        source_lang = self.config_manager.get('source_language', 'zh')
        target_lang = self.config_manager.get('target_language', 'en')
        self.source_lang_var.set(source_lang)
        self.target_lang_var.set(target_lang)
        self._update_language_labels()
    
    def _load_provider_config(self, provider: str) -> None:
        """Load configuration for a specific provider."""
        provider_config = self.config_manager.get_provider_config(provider)
        
        self.api_key_var.set(provider_config.api_key)
        
        # Set model if available
        if provider_config.model:
            self.model_var.set(provider_config.model)
    
    def get_config(self) -> dict:
        """Get current configuration.
        
        Returns:
            Dictionary containing current configuration
        """
        return {
            'provider': self.current_provider,
            'api_key': self.api_key_var.get(),
            'model': self.model_var.get(),
            'source_language': self.source_lang_var.get(),
            'target_language': self.target_lang_var.get(),
        }
    
    def save_config(self) -> None:
        """Save current configuration to config manager."""
        # Save provider settings
        provider_config = self.config_manager.get_provider_config(self.current_provider)
        provider_config.api_key = self.api_key_var.get()
        provider_config.model = self.model_var.get()
        provider_config.enabled = True
        self.config_manager.set_provider_config(self.current_provider, provider_config)
        
        # Save general settings
        self.config_manager.set('default_provider', self.current_provider)
        self.config_manager.set('source_language', self.source_lang_var.get())
        self.config_manager.set('target_language', self.target_lang_var.get())
        
        # Save to file
        self.config_manager.save()
    
    def _apply_theme(self) -> None:
        """Apply current theme colors to widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_secondary'])
