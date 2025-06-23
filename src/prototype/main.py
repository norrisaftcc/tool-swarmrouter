"""
SwarmRouter (Waggle) - MVP FastAPI Entrypoint

This module provides the main FastAPI application for the SwarmRouter prototype,
implementing a lightweight routing system for AI model requests between local
and cloud providers.

MVP Architecture:
- Local provider: LM Studio for fast, private inference
- Overflow providers: OpenRouter for broad model access, Azure for enterprise
- Simple load balancing and failover logic
- RESTful API compatible with OpenAI chat completions format

Stretch Goals (future iterations):
- Advanced load balancing algorithms
- Model-specific routing rules
- Request caching and optimization
- Comprehensive metrics and monitoring
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any, Optional
import logging

try:
    from .router import SwarmRouter
    from .config import Config
except ImportError:
    # Fallback for direct execution
    from router import SwarmRouter
    from config import Config

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SwarmRouter (Waggle)",
    description="AI Model Router - MVP for intelligent request routing",
    version="0.1.0-mvp"
)

# Initialize router with configuration
config = Config()
router = SwarmRouter(config)


@app.get("/")
async def root():
    """Root endpoint providing basic service information."""
    return {
        "service": "SwarmRouter",
        "codename": "waggle",
        "version": "0.1.0-mvp",
        "status": "active",
        "description": "AI model request router with local and cloud failover"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "providers": await router.get_provider_status()
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    OpenAI-compatible chat completions endpoint.
    
    Routes requests to the best available provider based on:
    - Current load and availability
    - Model requirements
    - Configured routing rules
    
    MVP Implementation:
    - Basic round-robin between local and overflow providers
    - Simple failover on errors
    - Request/response logging for debugging
    
    Stretch Goals:
    - Intelligent model-based routing
    - Request caching and deduplication
    - Advanced load balancing algorithms
    """
    try:
        # Parse request body
        body = await request.json()
        
        # Route the request through our router
        response = await router.route_chat_completion(body)
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat completion: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during request routing"
        )


@app.post("/admin/overflow_provider")
async def set_overflow_provider(provider_config: Dict[str, Any]):
    """
    Administrative endpoint to configure overflow providers.
    
    MVP Implementation:
    - Simple provider configuration updates
    - Basic validation of provider settings
    
    Stretch Goals:
    - Authentication and authorization
    - Provider health testing before activation
    - Gradual traffic shifting for provider changes
    """
    try:
        result = await router.configure_overflow_provider(provider_config)
        return {"status": "success", "result": result}
        
    except Exception as e:
        logger.error(f"Error configuring overflow provider: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to configure provider: {str(e)}"
        )


@app.get("/admin/status")
async def get_admin_status():
    """
    Administrative status endpoint providing detailed system information.
    
    Returns current routing configuration, provider health, and basic metrics.
    """
    try:
        status = await router.get_detailed_status()
        return status
        
    except Exception as e:
        logger.error(f"Error getting admin status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve system status"
        )


if __name__ == "__main__":
    # Development server configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )