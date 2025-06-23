"""
SwarmRouter (Waggle) - MVP Routing Logic

This module implements the core routing logic for distributing AI model requests
between local providers (LM Studio) and overflow cloud providers (OpenRouter, Azure).

MVP Architecture:
- Priority-based routing: Local first, then overflow providers
- Simple failover mechanism on provider errors
- Basic load tracking and provider health monitoring
- Configurable routing rules and provider weights

Stretch Goals (future iterations):
- Machine learning-based routing decisions
- Advanced load balancing algorithms (weighted round-robin, least connections)
- Model-specific routing optimization
- Request batching and optimization
- Comprehensive metrics and analytics
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from enum import Enum
import time
import random

try:
    from .adapters import LMStudioAdapter, OpenRouterAdapter, AzureAdapter
    from .config import Config
except ImportError:
    # Fallback for direct execution
    from adapters import LMStudioAdapter, OpenRouterAdapter, AzureAdapter
    from config import Config

logger = logging.getLogger(__name__)


class ProviderType(Enum):
    """Enumeration of supported provider types."""
    LOCAL = "local"
    OPENROUTER = "openrouter"
    AZURE = "azure"


class ProviderStatus(Enum):
    """Provider health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class SwarmRouter:
    """
    Main routing engine for the SwarmRouter system.
    
    Manages provider selection, load balancing, and failover logic
    for AI model requests in the MVP implementation.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the SwarmRouter with configuration.
        
        Args:
            config: Configuration object containing provider settings
        """
        self.config = config
        self.providers = {}
        self.provider_stats = {}
        self.last_health_check = 0
        
        # Initialize adapters for each provider type
        self._initialize_providers()
    
    def _initialize_providers(self):
        """
        Initialize provider adapters based on configuration.
        
        MVP Implementation:
        - LM Studio as primary local provider
        - OpenRouter as primary overflow provider
        - Azure as enterprise overflow option
        """
        # Initialize LM Studio (local provider)
        if self.config.lm_studio_enabled:
            self.providers[ProviderType.LOCAL] = LMStudioAdapter(
                base_url=self.config.lm_studio_url,
                timeout=self.config.local_timeout
            )
            self.provider_stats[ProviderType.LOCAL] = {
                "requests": 0,
                "errors": 0,
                "avg_response_time": 0,
                "status": ProviderStatus.HEALTHY
            }
        
        # Initialize OpenRouter (overflow provider)
        if self.config.openrouter_enabled:
            self.providers[ProviderType.OPENROUTER] = OpenRouterAdapter(
                api_key=self.config.openrouter_api_key,
                timeout=self.config.overflow_timeout
            )
            self.provider_stats[ProviderType.OPENROUTER] = {
                "requests": 0,
                "errors": 0,
                "avg_response_time": 0,
                "status": ProviderStatus.HEALTHY
            }
        
        # Initialize Azure (enterprise overflow provider)
        if self.config.azure_enabled:
            self.providers[ProviderType.AZURE] = AzureAdapter(
                endpoint=self.config.azure_endpoint,
                api_key=self.config.azure_api_key,
                timeout=self.config.overflow_timeout
            )
            self.provider_stats[ProviderType.AZURE] = {
                "requests": 0,
                "errors": 0,
                "avg_response_time": 0,
                "status": ProviderStatus.HEALTHY
            }
        
        logger.info(f"Initialized {len(self.providers)} providers")
    
    async def route_chat_completion(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a chat completion request to the best available provider.
        
        MVP Routing Logic:
        1. Try local provider first (LM Studio)
        2. Fall back to overflow providers on failure
        3. Simple round-robin between overflow providers
        
        Args:
            request_data: OpenAI-format chat completion request
            
        Returns:
            OpenAI-format chat completion response
            
        Raises:
            Exception: If all providers fail
        """
        start_time = time.time()
        
        # Determine routing order based on configuration and health
        routing_order = await self._get_routing_order(request_data)
        
        last_error = None
        
        for provider_type in routing_order:
            if provider_type not in self.providers:
                continue
                
            try:
                logger.info(f"Attempting request with provider: {provider_type.value}")
                
                provider = self.providers[provider_type]
                response = await provider.chat_completion(request_data)
                
                # Update success statistics
                self._update_provider_stats(provider_type, time.time() - start_time, success=True)
                
                logger.info(f"Successfully routed request via {provider_type.value}")
                return response
                
            except Exception as e:
                logger.warning(f"Provider {provider_type.value} failed: {str(e)}")
                self._update_provider_stats(provider_type, time.time() - start_time, success=False)
                last_error = e
                continue
        
        # All providers failed
        logger.error("All providers failed for request")
        raise Exception(f"All providers unavailable. Last error: {str(last_error)}")
    
    async def _get_routing_order(self, request_data: Dict[str, Any]) -> List[ProviderType]:
        """
        Determine the order in which to try providers for a request.
        
        MVP Implementation:
        - Local provider first (if healthy)
        - Overflow providers in configured order
        
        Stretch Goals:
        - Model-specific routing preferences
        - Load-based dynamic ordering
        - Geographic routing optimization
        
        Args:
            request_data: Request data for context-aware routing
            
        Returns:
            Ordered list of provider types to try
        """
        routing_order = []
        
        # Always try local first if available and healthy
        if (ProviderType.LOCAL in self.providers and 
            self.provider_stats[ProviderType.LOCAL]["status"] != ProviderStatus.UNAVAILABLE):
            routing_order.append(ProviderType.LOCAL)
        
        # Add overflow providers based on health and configuration
        overflow_providers = [
            ProviderType.OPENROUTER,
            ProviderType.AZURE
        ]
        
        # Filter to available and healthy providers
        available_overflow = [
            p for p in overflow_providers 
            if p in self.providers and 
            self.provider_stats[p]["status"] != ProviderStatus.UNAVAILABLE
        ]
        
        # Simple randomization for load distribution among overflow providers
        random.shuffle(available_overflow)
        routing_order.extend(available_overflow)
        
        return routing_order
    
    def _update_provider_stats(self, provider_type: ProviderType, response_time: float, success: bool):
        """
        Update provider statistics after a request attempt.
        
        Args:
            provider_type: The provider that was used
            response_time: Time taken for the request
            success: Whether the request succeeded
        """
        stats = self.provider_stats[provider_type]
        
        stats["requests"] += 1
        
        if success:
            # Update average response time (simple moving average)
            if stats["avg_response_time"] == 0:
                stats["avg_response_time"] = response_time
            else:
                stats["avg_response_time"] = (stats["avg_response_time"] + response_time) / 2
        else:
            stats["errors"] += 1
            
            # Mark as degraded if error rate is high
            error_rate = stats["errors"] / stats["requests"]
            if error_rate > 0.5:  # More than 50% error rate
                stats["status"] = ProviderStatus.DEGRADED
            if error_rate > 0.8:  # More than 80% error rate
                stats["status"] = ProviderStatus.UNAVAILABLE
    
    async def configure_overflow_provider(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure or reconfigure an overflow provider.
        
        MVP Implementation:
        - Basic provider configuration updates
        - Simple validation of required fields
        
        Args:
            provider_config: Provider configuration dictionary
            
        Returns:
            Configuration result
        """
        provider_type = provider_config.get("type")
        
        if provider_type == "openrouter":
            # Update OpenRouter configuration
            if "api_key" in provider_config:
                self.config.openrouter_api_key = provider_config["api_key"]
                
            # Reinitialize the provider
            self.providers[ProviderType.OPENROUTER] = OpenRouterAdapter(
                api_key=self.config.openrouter_api_key,
                timeout=self.config.overflow_timeout
            )
            
            return {"provider": "openrouter", "status": "configured"}
            
        elif provider_type == "azure":
            # Update Azure configuration
            if "endpoint" in provider_config:
                self.config.azure_endpoint = provider_config["endpoint"]
            if "api_key" in provider_config:
                self.config.azure_api_key = provider_config["api_key"]
                
            # Reinitialize the provider
            self.providers[ProviderType.AZURE] = AzureAdapter(
                endpoint=self.config.azure_endpoint,
                api_key=self.config.azure_api_key,
                timeout=self.config.overflow_timeout
            )
            
            return {"provider": "azure", "status": "configured"}
        
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
    
    async def get_provider_status(self) -> Dict[str, Any]:
        """
        Get current status of all providers.
        
        Returns:
            Dictionary with provider status information
        """
        status = {}
        
        for provider_type, stats in self.provider_stats.items():
            status[provider_type.value] = {
                "status": stats["status"].value,
                "requests": stats["requests"],
                "errors": stats["errors"],
                "error_rate": stats["errors"] / max(stats["requests"], 1),
                "avg_response_time": stats["avg_response_time"]
            }
        
        return status
    
    async def get_detailed_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status for administrative monitoring.
        
        Returns:
            Detailed status including configuration and metrics
        """
        return {
            "service": "SwarmRouter (Waggle)",
            "version": "0.1.0-mvp",
            "providers": await self.get_provider_status(),
            "configuration": {
                "local_enabled": self.config.lm_studio_enabled,
                "overflow_providers": [
                    p.value for p in [ProviderType.OPENROUTER, ProviderType.AZURE]
                    if p in self.providers
                ],
                "routing_strategy": "local_first_with_overflow"
            },
            "uptime": time.time() - self.last_health_check if self.last_health_check else 0
        }