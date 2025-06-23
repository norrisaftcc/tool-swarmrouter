"""
SwarmRouter (Waggle) - Configuration Management

This module handles configuration loading and management for the SwarmRouter MVP.
Supports environment variables, config files, and runtime configuration updates.

MVP Implementation:
- Simple environment variable-based configuration
- Basic validation and defaults
- Provider endpoint and authentication configuration

Stretch Goals (future iterations):
- Dynamic configuration reloading
- Configuration validation schemas
- Encrypted configuration storage
- Multi-environment configuration management
"""

import os
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """
    Configuration class for SwarmRouter (Waggle) MVP.
    
    Manages all configuration parameters including provider settings,
    timeouts, and routing behavior.
    """
    
    # Local Provider (LM Studio) Configuration
    lm_studio_enabled: bool = True
    lm_studio_url: str = "http://localhost:1234"
    local_timeout: int = 30
    
    # OpenRouter Configuration  
    openrouter_enabled: bool = True
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    
    # Azure OpenAI Configuration
    azure_enabled: bool = False
    azure_endpoint: Optional[str] = None
    azure_api_key: Optional[str] = None
    azure_api_version: str = "2023-12-01-preview"
    
    # General Configuration
    overflow_timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Logging Configuration
    log_level: str = "INFO"
    log_requests: bool = True
    log_responses: bool = False  # May contain sensitive data
    
    # Performance Configuration
    max_concurrent_requests: int = 10
    request_timeout: int = 300
    
    def __init__(self):
        """
        Initialize configuration from environment variables.
        
        MVP Implementation:
        - Load from environment variables with sensible defaults
        - Basic validation of required fields
        - Log configuration status for debugging
        """
        self._load_from_environment()
        self._validate_configuration()
        self._log_configuration_status()
    
    def _load_from_environment(self):
        """
        Load configuration values from environment variables.
        
        Environment variable naming convention:
        - SWARMROUTER_* for general settings
        - LMSTUDIO_* for local provider settings
        - OPENROUTER_* for OpenRouter settings
        - AZURE_* for Azure OpenAI settings
        """
        # Local Provider (LM Studio) Configuration
        self.lm_studio_enabled = self._get_bool_env("LMSTUDIO_ENABLED", self.lm_studio_enabled)
        self.lm_studio_url = os.getenv("LMSTUDIO_URL", self.lm_studio_url)
        self.local_timeout = self._get_int_env("LMSTUDIO_TIMEOUT", self.local_timeout)
        
        # OpenRouter Configuration
        self.openrouter_enabled = self._get_bool_env("OPENROUTER_ENABLED", self.openrouter_enabled)
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", self.openrouter_api_key)
        self.openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", self.openrouter_base_url)
        
        # Azure Configuration
        self.azure_enabled = self._get_bool_env("AZURE_ENABLED", self.azure_enabled)
        self.azure_endpoint = os.getenv("AZURE_ENDPOINT", self.azure_endpoint)
        self.azure_api_key = os.getenv("AZURE_API_KEY", self.azure_api_key)
        self.azure_api_version = os.getenv("AZURE_API_VERSION", self.azure_api_version)
        
        # General Configuration
        self.overflow_timeout = self._get_int_env("SWARMROUTER_OVERFLOW_TIMEOUT", self.overflow_timeout)
        self.max_retries = self._get_int_env("SWARMROUTER_MAX_RETRIES", self.max_retries)
        self.retry_delay = self._get_float_env("SWARMROUTER_RETRY_DELAY", self.retry_delay)
        
        # Logging Configuration
        self.log_level = os.getenv("SWARMROUTER_LOG_LEVEL", self.log_level)
        self.log_requests = self._get_bool_env("SWARMROUTER_LOG_REQUESTS", self.log_requests)
        self.log_responses = self._get_bool_env("SWARMROUTER_LOG_RESPONSES", self.log_responses)
        
        # Performance Configuration
        self.max_concurrent_requests = self._get_int_env("SWARMROUTER_MAX_CONCURRENT", self.max_concurrent_requests)
        self.request_timeout = self._get_int_env("SWARMROUTER_REQUEST_TIMEOUT", self.request_timeout)
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        """
        Get a boolean value from environment variable.
        
        Accepts: true, false, 1, 0, yes, no (case insensitive)
        """
        value = os.getenv(key, "").lower()
        if value in ["true", "1", "yes", "on"]:
            return True
        elif value in ["false", "0", "no", "off"]:
            return False
        else:
            return default
    
    def _get_int_env(self, key: str, default: int) -> int:
        """Get an integer value from environment variable."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Invalid integer value for {key}, using default: {default}")
            return default
    
    def _get_float_env(self, key: str, default: float) -> float:
        """Get a float value from environment variable."""
        try:
            return float(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Invalid float value for {key}, using default: {default}")
            return default
    
    def _validate_configuration(self):
        """
        Validate the loaded configuration.
        
        MVP Implementation:
        - Ensure at least one provider is enabled and configured
        - Validate required API keys for enabled providers
        - Check timeout and retry values are reasonable
        """
        errors = []
        
        # Validate that at least one provider is enabled
        enabled_providers = []
        
        if self.lm_studio_enabled:
            enabled_providers.append("LM Studio")
            # TODO: Could add URL validation here
        
        if self.openrouter_enabled:
            if not self.openrouter_api_key:
                errors.append("OpenRouter is enabled but OPENROUTER_API_KEY is not set")
            else:
                enabled_providers.append("OpenRouter")
        
        if self.azure_enabled:
            if not self.azure_endpoint:
                errors.append("Azure is enabled but AZURE_ENDPOINT is not set")
            if not self.azure_api_key:
                errors.append("Azure is enabled but AZURE_API_KEY is not set")
            if self.azure_endpoint and self.azure_api_key:
                enabled_providers.append("Azure")
        
        if not enabled_providers:
            errors.append("No providers are properly configured and enabled")
        
        # Validate timeout values
        if self.local_timeout <= 0:
            errors.append("Local timeout must be positive")
        
        if self.overflow_timeout <= 0:
            errors.append("Overflow timeout must be positive")
        
        if self.request_timeout <= 0:
            errors.append("Request timeout must be positive")
        
        # Validate retry settings
        if self.max_retries < 0:
            errors.append("Max retries cannot be negative")
        
        if self.retry_delay < 0:
            errors.append("Retry delay cannot be negative")
        
        # Validate performance settings
        if self.max_concurrent_requests <= 0:
            errors.append("Max concurrent requests must be positive")
        
        if errors:
            error_message = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
            logger.error(error_message)
            raise ValueError(error_message)
        
        logger.info(f"Configuration validated successfully. Enabled providers: {', '.join(enabled_providers)}")
    
    def _log_configuration_status(self):
        """
        Log the current configuration status for debugging.
        
        Note: Sensitive information like API keys are not logged.
        """
        logger.info("SwarmRouter (Waggle) Configuration:")
        logger.info(f"  LM Studio: {'enabled' if self.lm_studio_enabled else 'disabled'} ({self.lm_studio_url})")
        logger.info(f"  OpenRouter: {'enabled' if self.openrouter_enabled else 'disabled'} ({'configured' if self.openrouter_api_key else 'no API key'})")
        logger.info(f"  Azure: {'enabled' if self.azure_enabled else 'disabled'} ({'configured' if self.azure_endpoint and self.azure_api_key else 'incomplete config'})")
        logger.info(f"  Timeouts: local={self.local_timeout}s, overflow={self.overflow_timeout}s")
        logger.info(f"  Performance: max_concurrent={self.max_concurrent_requests}, request_timeout={self.request_timeout}s")
    
    def get_provider_config(self, provider_type: str) -> Dict[str, Any]:
        """
        Get configuration dictionary for a specific provider.
        
        Args:
            provider_type: Type of provider ("lmstudio", "openrouter", "azure")
            
        Returns:
            Configuration dictionary for the provider
        """
        if provider_type.lower() == "lmstudio":
            return {
                "enabled": self.lm_studio_enabled,
                "url": self.lm_studio_url,
                "timeout": self.local_timeout
            }
        
        elif provider_type.lower() == "openrouter":
            return {
                "enabled": self.openrouter_enabled,
                "api_key": self.openrouter_api_key,
                "base_url": self.openrouter_base_url,
                "timeout": self.overflow_timeout
            }
        
        elif provider_type.lower() == "azure":
            return {
                "enabled": self.azure_enabled,
                "endpoint": self.azure_endpoint,
                "api_key": self.azure_api_key,
                "api_version": self.azure_api_version,
                "timeout": self.overflow_timeout
            }
        
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
    
    def update_provider_config(self, provider_type: str, config_updates: Dict[str, Any]):
        """
        Update configuration for a specific provider.
        
        MVP Implementation:
        - Simple attribute updates
        - Basic validation
        
        Stretch Goals:
        - Configuration persistence
        - Atomic updates with rollback
        - Configuration change notifications
        
        Args:
            provider_type: Type of provider to update
            config_updates: Dictionary of configuration updates
        """
        if provider_type.lower() == "lmstudio":
            if "url" in config_updates:
                self.lm_studio_url = config_updates["url"]
            if "timeout" in config_updates:
                self.local_timeout = config_updates["timeout"]
            if "enabled" in config_updates:
                self.lm_studio_enabled = config_updates["enabled"]
                
        elif provider_type.lower() == "openrouter":
            if "api_key" in config_updates:
                self.openrouter_api_key = config_updates["api_key"]
            if "base_url" in config_updates:
                self.openrouter_base_url = config_updates["base_url"]
            if "timeout" in config_updates:
                self.overflow_timeout = config_updates["timeout"]
            if "enabled" in config_updates:
                self.openrouter_enabled = config_updates["enabled"]
                
        elif provider_type.lower() == "azure":
            if "endpoint" in config_updates:
                self.azure_endpoint = config_updates["endpoint"]
            if "api_key" in config_updates:
                self.azure_api_key = config_updates["api_key"]
            if "api_version" in config_updates:
                self.azure_api_version = config_updates["api_version"]
            if "timeout" in config_updates:
                self.overflow_timeout = config_updates["timeout"]
            if "enabled" in config_updates:
                self.azure_enabled = config_updates["enabled"]
        
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
        
        # Re-validate configuration after updates
        self._validate_configuration()
        
        logger.info(f"Updated configuration for {provider_type}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary format.
        
        Note: Sensitive fields like API keys are excluded for security.
        
        Returns:
            Configuration dictionary suitable for logging/debugging
        """
        return {
            "lm_studio": {
                "enabled": self.lm_studio_enabled,
                "url": self.lm_studio_url,
                "timeout": self.local_timeout
            },
            "openrouter": {
                "enabled": self.openrouter_enabled,
                "base_url": self.openrouter_base_url,
                "timeout": self.overflow_timeout,
                "api_key_configured": bool(self.openrouter_api_key)
            },
            "azure": {
                "enabled": self.azure_enabled,
                "endpoint": self.azure_endpoint,
                "api_version": self.azure_api_version,
                "timeout": self.overflow_timeout,
                "api_key_configured": bool(self.azure_api_key)
            },
            "general": {
                "max_retries": self.max_retries,
                "retry_delay": self.retry_delay,
                "log_level": self.log_level,
                "max_concurrent_requests": self.max_concurrent_requests,
                "request_timeout": self.request_timeout
            }
        }