"""
SwarmRouter (Waggle) - MVP Prototype Package

This package contains the initial MVP implementation of SwarmRouter,
an intelligent AI model routing system designed to distribute requests
between local inference servers and cloud providers.

The system operates under the code name "waggle" for development purposes.

Module Overview:
- main.py: FastAPI application and API endpoints
- router.py: Core routing logic and provider orchestration
- adapters.py: Provider-specific API adapters
- config.py: Configuration management and validation

Version: 0.1.0-mvp
Status: Initial scaffolding and documentation
"""

__version__ = "0.1.0-mvp"
__codename__ = "waggle"
__author__ = "SwarmRouter Team"
__description__ = "Intelligent AI model routing system with local and cloud failover"

# Import main components for easy access
from .config import Config
from .router import SwarmRouter
from .adapters import LMStudioAdapter, OpenRouterAdapter, AzureAdapter

__all__ = [
    "Config",
    "SwarmRouter", 
    "LMStudioAdapter",
    "OpenRouterAdapter",
    "AzureAdapter"
]