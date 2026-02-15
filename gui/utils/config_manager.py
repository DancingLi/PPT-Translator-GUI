"""Configuration manager for PPT Translator GUI.

Provides centralized configuration management with secure API key storage,
user preferences, and application settings.
"""

import json
import os
import base64
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


# Try to import Windows DPAPI for secure key storage
try:
    import ctypes
    from ctypes import wintypes
    _WINDOWS_AVAILABLE = True
except ImportError:
    _WINDOWS_AVAILABLE = False


@dataclass
class ProviderConfig:
    """Configuration for a translation provider."""
    api_key: str = ''
    api_base: str = ''
    model: str = ''
    enabled: bool = False


@dataclass
class AppConfig:
    """Application configuration data class."""
    # General settings
    theme: str = 'dark'
    language: str = 'zh'
    auto_update: bool = True
    
    # Translation settings
    default_provider: str = 'openai'
    source_language: str = 'zh'
    target_language: str = 'en'
    
    # Advanced settings
    max_workers: int = 4
    max_chunk_size: int = 1000
    output_directory: str = ''
    keep_intermediate: bool = False
    
    # Window settings
    window_width: int = 1000
    window_height: int = 700
    window_maximized: bool = False
    
    # Provider configurations
    providers: Dict[str, ProviderConfig] = None
    
    def __post_init__(self):
        """Initialize default provider configs if not set."""
        if self.providers is None:
            self.providers = {
                'openai': ProviderConfig(),
                'anthropic': ProviderConfig(),
                'deepseek': ProviderConfig(),
                'grok': ProviderConfig(),
                'gemini': ProviderConfig(),
            }


class ConfigManager:
    """Manages application configuration and settings.
    
    Provides centralized access to user preferences, secure API key storage,
    and application settings with automatic persistence.
    
    Attributes:
        config_dir: Directory for configuration files
        config_file: Path to main configuration file
        config: Current application configuration
    
    Example:
        >>> config_manager = ConfigManager()
        >>> config_manager.set('theme', 'dark')
        >>> config_manager.save()
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_dir: Custom configuration directory.
                       Defaults to %APPDATA%/PPTTranslator
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Use %APPDATA% on Windows, ~/.config on others
            appdata = os.environ.get('APPDATA')
            if appdata:
                self.config_dir = Path(appdata) / 'PPTTranslator'
            else:
                self.config_dir = Path.home() / '.config' / 'ppttranslator'
        
        self.config_file = self.config_dir / 'config.json'
        self._config = AppConfig()
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing config if available
        self.load()
    
    def load(self) -> bool:
        """Load configuration from file.
        
        Returns:
            True if configuration was loaded successfully, False otherwise
        """
        if not self.config_file.exists():
            return False
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Decrypt API keys
            if 'providers' in data:
                for provider, config in data['providers'].items():
                    if 'api_key' in config and config['api_key']:
                        try:
                            config['api_key'] = self._decrypt_key(config['api_key'])
                        except Exception:
                            # If decryption fails, keep as is
                            pass
            
            # Update config from loaded data
            self._config = self._dict_to_config(data)
            return True
            
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
    
    def save(self) -> bool:
        """Save configuration to file.
        
        Returns:
            True if configuration was saved successfully, False otherwise
        """
        try:
            data = self._config_to_dict(self._config)
            
            # Encrypt API keys
            if 'providers' in data:
                for provider, config in data['providers'].items():
                    if 'api_key' in config and config['api_key']:
                        try:
                            config['api_key'] = self._encrypt_key(config['api_key'])
                        except Exception:
                            # If encryption fails, keep as is
                            pass
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Supports nested keys using dot notation (e.g., 'providers.openai.api_key').
        
        Args:
            key: Configuration key (supports dot notation for nested values)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            elif hasattr(value, k):
                value = getattr(value, k, default)
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key.
        
        Supports nested keys using dot notation (e.g., 'providers.openai.api_key').
        
        Args:
            key: Configuration key (supports dot notation for nested values)
            value: Value to set
        """
        keys = key.split('.')
        target = self._config
        
        # Navigate to the parent of the target
        for k in keys[:-1]:
            if isinstance(target, dict):
                if k not in target:
                    target[k] = {}
                target = target[k]
            elif hasattr(target, k):
                target = getattr(target, k)
            else:
                return
        
        # Set the value
        last_key = keys[-1]
        if isinstance(target, dict):
            target[last_key] = value
        elif hasattr(target, last_key):
            setattr(target, last_key, value)
    
    def get_provider_config(self, provider: str) -> ProviderConfig:
        """Get configuration for a specific provider.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            
        Returns:
            ProviderConfig instance
        """
        if provider not in self._config.providers:
            self._config.providers[provider] = ProviderConfig()
        return self._config.providers[provider]
    
    def set_provider_config(self, provider: str, config: ProviderConfig) -> None:
        """Set configuration for a specific provider.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            config: ProviderConfig instance
        """
        self._config.providers[provider] = config
    
    def _encrypt_key(self, key: str) -> str:
        """Encrypt API key using Windows DPAPI.
        
        Args:
            key: Plain text API key
            
        Returns:
            Base64 encoded encrypted key
        """
        if not _WINDOWS_AVAILABLE or not key:
            return key
        
        try:
            # Convert string to bytes
            data = key.encode('utf-8')
            
            # Use Windows DPAPI to encrypt
            # CRYPTPROTECT_LOCAL_MACHINE = 0x4
            # CRYPTPROTECT_UI_FORBIDDEN = 0x1
            blob_in = ctypes.create_string_buffer(data)
            blob_out = ctypes.c_void_p()
            
            # Call CryptProtectData
            ctypes.windll.crypt32.CryptProtectData(
                ctypes.byref(ctypes.c_ulong(len(data))),
                ctypes.c_wchar_p('PPTTranslatorAPIKey'),
                None,
                None,
                None,
                0x1,  # CRYPTPROTECT_UI_FORBIDDEN
                ctypes.byref(blob_out)
            )
            
            # Get encrypted data
            encrypted_len = ctypes.c_ulong(0)
            ctypes.windll.crypt32.CryptUnprotectData(
                blob_out,
                None,
                None,
                None,
                None,
                0x1,
                ctypes.byref(encrypted_len)
            )
            
            # Encode as base64
            encrypted_data = ctypes.string_at(blob_out, encrypted_len.value)
            return base64.b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            print(f"Warning: Could not encrypt API key: {e}")
            return key
    
    def _decrypt_key(self, encrypted_key: str) -> str:
        """Decrypt API key using Windows DPAPI.
        
        Args:
            encrypted_key: Base64 encoded encrypted key
            
        Returns:
            Decrypted plain text key
        """
        if not _WINDOWS_AVAILABLE or not encrypted_key:
            return encrypted_key
        
        try:
            # Decode from base64
            encrypted_data = base64.b64decode(encrypted_key)
            
            # Use Windows DPAPI to decrypt
            blob_in = ctypes.create_string_buffer(encrypted_data)
            blob_out = ctypes.c_void_p()
            
            # Call CryptUnprotectData
            ctypes.windll.crypt32.CryptUnprotectData(
                ctypes.byref(ctypes.c_ulong(len(encrypted_data))),
                None,
                None,
                None,
                None,
                0x1,  # CRYPTPROTECT_UI_FORBIDDEN
                ctypes.byref(blob_out)
            )
            
            # Get decrypted data
            decrypted_len = ctypes.c_ulong(0)
            ctypes.windll.crypt32.CryptUnprotectData(
                blob_out,
                None,
                None,
                None,
                None,
                0x1,
                ctypes.byref(decrypted_len)
            )
            
            decrypted_data = ctypes.string_at(blob_out, decrypted_len.value)
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            print(f"Warning: Could not decrypt API key: {e}")
            return encrypted_key
    
    def _config_to_dict(self, config: AppConfig) -> dict:
        """Convert AppConfig to dictionary."""
        data = {
            'theme': config.theme,
            'language': config.language,
            'auto_update': config.auto_update,
            'default_provider': config.default_provider,
            'source_language': config.source_language,
            'target_language': config.target_language,
            'max_workers': config.max_workers,
            'max_chunk_size': config.max_chunk_size,
            'output_directory': config.output_directory,
            'keep_intermediate': config.keep_intermediate,
            'window_width': config.window_width,
            'window_height': config.window_height,
            'window_maximized': config.window_maximized,
            'providers': {}
        }
        
        for name, provider_config in config.providers.items():
            data['providers'][name] = {
                'api_key': provider_config.api_key,
                'api_base': provider_config.api_base,
                'model': provider_config.model,
                'enabled': provider_config.enabled
            }
        
        return data
    
    def _dict_to_config(self, data: dict) -> AppConfig:
        """Convert dictionary to AppConfig."""
        config = AppConfig()
        
        config.theme = data.get('theme', 'dark')
        config.language = data.get('language', 'zh')
        config.auto_update = data.get('auto_update', True)
        config.default_provider = data.get('default_provider', 'openai')
        config.source_language = data.get('source_language', 'zh')
        config.target_language = data.get('target_language', 'en')
        config.max_workers = data.get('max_workers', 4)
        config.max_chunk_size = data.get('max_chunk_size', 1000)
        config.output_directory = data.get('output_directory', '')
        config.keep_intermediate = data.get('keep_intermediate', False)
        config.window_width = data.get('window_width', 1000)
        config.window_height = data.get('window_height', 700)
        config.window_maximized = data.get('window_maximized', False)
        
        # Load provider configs
        providers_data = data.get('providers', {})
        for name, provider_data in providers_data.items():
            config.providers[name] = ProviderConfig(
                api_key=provider_data.get('api_key', ''),
                api_base=provider_data.get('api_base', ''),
                model=provider_data.get('model', ''),
                enabled=provider_data.get('enabled', False)
            )
        
        return config


# Global config manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get global config manager instance.
    
    Creates a new instance if one doesn't exist.
    
    Returns:
        Global ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def set_config_manager(manager: ConfigManager) -> None:
    """Set global config manager instance.
    
    Args:
        manager: ConfigManager instance to use globally
    """
    global _config_manager
    _config_manager = manager