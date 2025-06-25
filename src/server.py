#!/usr/bin/env python3
"""
Shadow Clone Jutsu MCP Server - FastAPI Implementation

This server demonstrates task delegation using the Shadow Clone Jutsu metaphor
from Naruto, where specialized shadow clones are created to handle different
types of tasks efficiently through parallel execution.

The Shadow Clone Jutsu allows a ninja to create multiple copies of themselves,
each capable of working independently on different tasks while sharing the
original's knowledge and abilities. When a clone completes its task, the
knowledge and experience gained is transferred back to the original.

This maps to project management and task delegation by:
- Creating specialized "clones" for different task types
- Parallel execution of subtasks
- Knowledge consolidation and reporting
- Efficient resource utilization through smart delegation
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    # Fallback for development without FastAPI installed
    print("Warning: FastAPI not installed. Install with: pip install fastapi uvicorn")
    FASTAPI_AVAILABLE = False
    FastAPI = None
    HTTPException = None
    JSONResponse = None
    uvicorn = None

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Shadow Clone Jutsu MCP Server",
        description="Task delegation server using the Shadow Clone Jutsu metaphor for efficient parallel task execution",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
else:
    app = None
    logger.warning("Running without FastAPI (development mode)")


def create_root_response() -> Dict[str, Any]:
    """Create the root endpoint response."""
    return {
        "message": "🥷 Welcome to the Shadow Clone Jutsu MCP Server! 🥷",
        "description": "Master the art of task delegation through shadow clone techniques",
        "jutsu_info": {
            "technique": "Multi Shadow Clone Jutsu (Taju Kage Bunshin no Jutsu)",
            "purpose": "Create specialized clones to handle complex tasks in parallel",
            "benefit": "Multiply your productivity by delegating work to shadow clones"
        },
        "server_info": {
            "name": "Shadow Clone Jutsu MCP Server",
            "version": "0.1.0",
            "status": "ready",
            "timestamp": datetime.now().isoformat()
        },
        "available_endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "motto": "A ninja who breaks the rules is scum, but a ninja who abandons their teammates is worse than scum!"
    }


def create_health_response() -> Dict[str, Any]:
    """Create the health endpoint response."""
    return {
        "status": "healthy",
        "service": "Shadow Clone Jutsu MCP Server",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat(),
        "chakra_level": "maximum",
        "clone_capacity": "unlimited",
        "ready_for_missions": True
    }


if FASTAPI_AVAILABLE and app:
    @app.get("/")
    async def root() -> Dict[str, Any]:
        """
        Root endpoint providing a welcome message for the Shadow Clone Jutsu MCP Server.
        
        Returns a greeting message explaining the server's purpose and capabilities,
        along with basic server information and status.
        
        Returns:
            Dict containing welcome message and server metadata
        """
        return create_root_response()


    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """
        Health check endpoint for monitoring and load balancers.
        
        Returns the current health status of the Shadow Clone Jutsu server,
        including basic system information and readiness status.
        
        Returns:
            Dict containing health status and system information
        """
        return create_health_response()


if __name__ == "__main__":
    # Development server configuration
    logger.info("🥷 Starting Shadow Clone Jutsu MCP Server...")
    logger.info("Ready to create shadow clones for task delegation!")
    
    if FASTAPI_AVAILABLE and uvicorn and app:
        uvicorn.run(
            "server:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    else:
        logger.info("Demo mode - FastAPI not available")
        print("🥷 Shadow Clone Jutsu MCP Server (Demo Mode)")
        print("Root endpoint response:")
        import json
        print(json.dumps(create_root_response(), indent=2))
        print("\nHealth endpoint response:")
        print(json.dumps(create_health_response(), indent=2))