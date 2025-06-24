#!/usr/bin/env python3
"""
Entry point for running the SwarmRouter MCP server.

This allows the server to be run with:
  python -m src
  python -m src.server
"""

if __name__ == "__main__":
    from . import server
    # The server module will handle the rest