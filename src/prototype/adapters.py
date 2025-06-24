"""
SwarmRouter (Waggle) - Model API Adapters

This module provides adapter classes for different AI model providers,
implementing a common interface for chat completions while handling
provider-specific authentication, request formatting, and response parsing.

MVP Architecture:
- LMStudioAdapter: Local inference via LM Studio
- OpenRouterAdapter: Cloud inference via OpenRouter
- AzureAdapter: Enterprise inference via Azure OpenAI

Each adapter normalizes provider APIs to a common OpenAI-compatible interface
for seamless routing and failover between providers.

Stretch Goals (future iterations):
- Streaming response support
- Provider-specific optimization (batching, caching)
- Advanced error handling and retry logic
- Model capability detection and routing
- Request/response transformation pipelines
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional, AsyncGenerator
from abc import ABC, abstractmethod
import json
import time

logger = logging.getLogger(__name__)


class ProviderAdapter(ABC):
    """
    Abstract base class for AI model provider adapters.
    
    Defines the common interface that all provider adapters must implement
    for consistent routing behavior across different providers.
    """
    
    def __init__(self, timeout: int = 60):
        """
        Initialize the adapter with common configuration.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _ensure_session(self):
        """Ensure aiohttp session is initialized."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
    
    async def close(self):
        """Clean up resources."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    @abstractmethod
    async def chat_completion(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a chat completion request.
        
        Args:
            request_data: OpenAI-format chat completion request
            
        Returns:
            OpenAI-format chat completion response
            
        Raises:
            Exception: If the request fails
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the provider is healthy and available.
        
        Returns:
            True if provider is healthy, False otherwise
        """
        pass


class LMStudioAdapter(ProviderAdapter):
    """
    Adapter for LM Studio local inference server.
    
    LM Studio provides OpenAI-compatible API endpoints for local model inference,
    making this adapter relatively straightforward as it mostly forwards requests.
    
    MVP Implementation:
    - Direct request forwarding to LM Studio
    - Basic error handling and timeout management
    - Health checking via server status endpoint
    
    Stretch Goals:
    - Model loading/unloading management
    - Local model capability detection
    - Performance optimization for local inference
    """
    
    def __init__(self, base_url: str = "http://localhost:1234", timeout: int = 30):
        """
        Initialize LM Studio adapter.
        
        Args:
            base_url: LM Studio server URL
            timeout: Request timeout in seconds
        """
        super().__init__(timeout)
        self.base_url = base_url.rstrip('/')
        self.chat_url = f"{self.base_url}/v1/chat/completions"
        self.models_url = f"{self.base_url}/v1/models"
    
    async def chat_completion(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forward chat completion request to LM Studio.
        
        LM Studio uses OpenAI-compatible format, so we can forward requests directly
        with minimal transformation.
        """
        await self._ensure_session()
        
        try:
            logger.debug(f"Sending request to LM Studio: {self.chat_url}")
            
            async with self.session.post(
                self.chat_url,
                json=request_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.debug("LM Studio request successful")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"LM Studio error {response.status}: {error_text}")
                    raise Exception(f"LM Studio API error: {response.status} - {error_text}")
                    
        except asyncio.TimeoutError:
            logger.error("LM Studio request timeout")
            raise Exception("LM Studio request timeout")
        except aiohttp.ClientError as e:
            logger.error(f"LM Studio connection error: {str(e)}")
            raise Exception(f"LM Studio connection error: {str(e)}")
    
    async def health_check(self) -> bool:
        """
        Check LM Studio server health by querying available models.
        
        Returns:
            True if server is responding and has models available
        """
        await self._ensure_session()
        
        try:
            async with self.session.get(self.models_url) as response:
                if response.status == 200:
                    models_data = await response.json()
                    # Check if any models are available
                    models = models_data.get("data", [])
                    is_healthy = len(models) > 0
                    logger.debug(f"LM Studio health check: {'healthy' if is_healthy else 'no models'} ({len(models)} models)")
                    return is_healthy
                else:
                    logger.warning(f"LM Studio health check failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.warning(f"LM Studio health check error: {str(e)}")
            return False


class OpenRouterAdapter(ProviderAdapter):
    """
    Adapter for OpenRouter cloud AI service.
    
    OpenRouter provides access to multiple AI models through a unified API,
    with OpenAI-compatible endpoints and authentication via API keys.
    
    MVP Implementation:
    - API key authentication
    - Request forwarding with proper headers
    - Error handling and rate limit management
    
    Stretch Goals:
    - Model preference and fallback logic
    - Cost optimization and tracking
    - Advanced routing based on model capabilities
    """
    
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1", timeout: int = 60):
        """
        Initialize OpenRouter adapter.
        
        Args:
            api_key: OpenRouter API key
            base_url: OpenRouter API base URL
            timeout: Request timeout in seconds
        """
        super().__init__(timeout)
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.chat_url = f"{self.base_url}/chat/completions"
        self.models_url = f"{self.base_url}/models"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for OpenRouter requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/norrisaftcc/tool-swarmrouter",  # Required by OpenRouter
            "X-Title": "SwarmRouter (Waggle)"  # Optional but helpful for tracking
        }
    
    async def chat_completion(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forward chat completion request to OpenRouter.
        
        OpenRouter uses OpenAI-compatible format with additional features
        like model selection and routing preferences.
        """
        await self._ensure_session()
        
        try:
            # Ensure we have a model specified (OpenRouter requires this)
            if "model" not in request_data:
                request_data["model"] = "openai/gpt-3.5-turbo"  # Default fallback
            
            logger.debug(f"Sending request to OpenRouter: {request_data.get('model', 'unknown')}")
            
            async with self.session.post(
                self.chat_url,
                json=request_data,
                headers=self._get_headers()
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.debug("OpenRouter request successful")
                    return result
                elif response.status == 429:
                    # Rate limit exceeded
                    logger.warning("OpenRouter rate limit exceeded")
                    raise Exception("OpenRouter rate limit exceeded")
                elif response.status == 401:
                    # Authentication error
                    logger.error("OpenRouter authentication failed")
                    raise Exception("OpenRouter authentication failed")
                else:
                    error_text = await response.text()
                    logger.error(f"OpenRouter error {response.status}: {error_text}")
                    raise Exception(f"OpenRouter API error: {response.status} - {error_text}")
                    
        except asyncio.TimeoutError:
            logger.error("OpenRouter request timeout")
            raise Exception("OpenRouter request timeout")
        except aiohttp.ClientError as e:
            logger.error(f"OpenRouter connection error: {str(e)}")
            raise Exception(f"OpenRouter connection error: {str(e)}")
    
    async def health_check(self) -> bool:
        """
        Check OpenRouter service health by querying available models.
        
        Returns:
            True if service is responding and accessible
        """
        await self._ensure_session()
        
        try:
            async with self.session.get(
                self.models_url,
                headers=self._get_headers()
            ) as response:
                
                if response.status == 200:
                    models_data = await response.json()
                    # Check if models are available
                    models = models_data.get("data", [])
                    is_healthy = len(models) > 0
                    logger.debug(f"OpenRouter health check: {'healthy' if is_healthy else 'no models'} ({len(models)} models)")
                    return is_healthy
                elif response.status == 401:
                    logger.warning("OpenRouter health check: authentication failed")
                    return False
                else:
                    logger.warning(f"OpenRouter health check failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.warning(f"OpenRouter health check error: {str(e)}")
            return False


class AzureAdapter(ProviderAdapter):
    """
    Adapter for Azure OpenAI Service.
    
    Azure OpenAI provides enterprise-grade AI services with OpenAI models,
    featuring enhanced security, compliance, and integration with Azure services.
    
    MVP Implementation:
    - Azure-specific authentication and endpoint handling
    - API version management
    - Basic request/response handling
    
    Stretch Goals:
    - Azure-specific features (content filtering, etc.)
    - Integration with Azure monitoring and logging
    - Multi-region deployment support
    """
    
    def __init__(self, endpoint: str, api_key: str, api_version: str = "2023-12-01-preview", timeout: int = 60):
        """
        Initialize Azure OpenAI adapter.
        
        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            api_version: Azure OpenAI API version
            timeout: Request timeout in seconds
        """
        super().__init__(timeout)
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key
        self.api_version = api_version
        
        # Azure uses deployment-specific URLs
        # For MVP, we'll use a default deployment name that can be configured
        self.default_deployment = "gpt-35-turbo"  # Common Azure deployment name
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for Azure OpenAI requests."""
        return {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _get_chat_url(self, deployment_name: str) -> str:
        """
        Get the chat completions URL for a specific deployment.
        
        Azure uses deployment-specific endpoints rather than model names.
        """
        return f"{self.endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={self.api_version}"
    
    async def chat_completion(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forward chat completion request to Azure OpenAI.
        
        Azure OpenAI uses a slightly different URL structure with deployments
        instead of model names in the URL path.
        """
        await self._ensure_session()
        
        try:
            # Extract deployment name from model field or use default
            deployment_name = self._extract_deployment_name(request_data.get("model", self.default_deployment))
            
            # Remove model from request data as Azure doesn't expect it in the body
            azure_request = request_data.copy()
            if "model" in azure_request:
                del azure_request["model"]
            
            chat_url = self._get_chat_url(deployment_name)
            logger.debug(f"Sending request to Azure OpenAI: {deployment_name}")
            
            async with self.session.post(
                chat_url,
                json=azure_request,
                headers=self._get_headers()
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.debug("Azure OpenAI request successful")
                    return result
                elif response.status == 429:
                    # Rate limit or quota exceeded
                    logger.warning("Azure OpenAI rate limit exceeded")
                    raise Exception("Azure OpenAI rate limit exceeded")
                elif response.status == 401:
                    # Authentication error
                    logger.error("Azure OpenAI authentication failed")
                    raise Exception("Azure OpenAI authentication failed")
                else:
                    error_text = await response.text()
                    logger.error(f"Azure OpenAI error {response.status}: {error_text}")
                    raise Exception(f"Azure OpenAI API error: {response.status} - {error_text}")
                    
        except asyncio.TimeoutError:
            logger.error("Azure OpenAI request timeout")
            raise Exception("Azure OpenAI request timeout")
        except aiohttp.ClientError as e:
            logger.error(f"Azure OpenAI connection error: {str(e)}")
            raise Exception(f"Azure OpenAI connection error: {str(e)}")
    
    def _extract_deployment_name(self, model_name: str) -> str:
        """
        Extract Azure deployment name from model name.
        
        MVP Implementation:
        - Simple mapping of common model names to deployment names
        - Fallback to default deployment
        
        Stretch Goals:
        - Dynamic deployment discovery
        - Model-to-deployment mapping configuration
        """
        # Simple model name to deployment mapping
        model_mapping = {
            "gpt-3.5-turbo": "gpt-35-turbo",
            "gpt-4": "gpt-4",
            "gpt-4-turbo": "gpt-4-turbo",
            "gpt-4o": "gpt-4o"
        }
        
        return model_mapping.get(model_name, self.default_deployment)
    
    async def health_check(self) -> bool:
        """
        Check Azure OpenAI service health.
        
        Since Azure doesn't have a models endpoint, we'll do a minimal
        test request to check connectivity and authentication.
        """
        await self._ensure_session()
        
        try:
            # Make a minimal chat completion request to test connectivity
            test_request = {
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1
            }
            
            chat_url = self._get_chat_url(self.default_deployment)
            
            async with self.session.post(
                chat_url,
                json=test_request,
                headers=self._get_headers()
            ) as response:
                
                # Accept both success and quota exceeded as "healthy"
                # (quota exceeded means the service is working, just at capacity)
                is_healthy = response.status in [200, 429]
                logger.debug(f"Azure OpenAI health check: {'healthy' if is_healthy else 'unhealthy'} (status: {response.status})")
                return is_healthy
                    
        except Exception as e:
            logger.warning(f"Azure OpenAI health check error: {str(e)}")
            return False


# Factory function for creating adapters
def create_adapter(provider_type: str, **config) -> ProviderAdapter:
    """
    Factory function to create provider adapters.
    
    Args:
        provider_type: Type of provider ("lmstudio", "openrouter", "azure")
        **config: Provider-specific configuration parameters
        
    Returns:
        Configured provider adapter instance
        
    Raises:
        ValueError: If provider type is not supported
    """
    if provider_type.lower() == "lmstudio":
        return LMStudioAdapter(
            base_url=config.get("base_url", "http://localhost:1234"),
            timeout=config.get("timeout", 30)
        )
    
    elif provider_type.lower() == "openrouter":
        if "api_key" not in config:
            raise ValueError("OpenRouter adapter requires 'api_key' parameter")
        
        return OpenRouterAdapter(
            api_key=config["api_key"],
            base_url=config.get("base_url", "https://openrouter.ai/api/v1"),
            timeout=config.get("timeout", 60)
        )
    
    elif provider_type.lower() == "azure":
        if "endpoint" not in config or "api_key" not in config:
            raise ValueError("Azure adapter requires 'endpoint' and 'api_key' parameters")
        
        return AzureAdapter(
            endpoint=config["endpoint"],
            api_key=config["api_key"],
            api_version=config.get("api_version", "2023-12-01-preview"),
            timeout=config.get("timeout", 60)
        )
    
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")


# Cleanup utility for graceful shutdown
async def cleanup_adapters(*adapters: ProviderAdapter):
    """
    Clean up multiple adapter instances.
    
    Args:
        *adapters: Variable number of adapter instances to clean up
    """
    for adapter in adapters:
        try:
            await adapter.close()
        except Exception as e:
            logger.warning(f"Error cleaning up adapter: {str(e)}")