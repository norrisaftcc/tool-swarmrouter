#!/bin/bash
# 
# SwarmRouter Minimal MVP - Quick Start Script
#
# This script helps you quickly get started with the minimal MCP server implementation.
#

set -e

echo "🐝 SwarmRouter Minimal MVP - Quick Start"
echo "========================================"
echo

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "✅ Python $PYTHON_VERSION detected (>= $REQUIRED_VERSION required)"
else
    echo "❌ Python $PYTHON_VERSION detected, but >= $REQUIRED_VERSION required"
    exit 1
fi

# Navigate to the swarmrouter-mcp directory
cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -f "minimal_mcp_server.py" ]; then
    echo "❌ Error: minimal_mcp_server.py not found"
    echo "   Make sure you're running this script from the swarmrouter-mcp directory"
    exit 1
fi

echo "📁 Working directory: $(pwd)"
echo

# Install minimal dependencies
echo "📦 Installing minimal dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements_minimal.txt --user
elif command -v pip &> /dev/null; then
    pip install -r requirements_minimal.txt --user
else
    echo "❌ Error: pip not found. Please install pip and try again."
    exit 1
fi

echo "✅ Dependencies installed"
echo

# Check for Anthropic API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ℹ️  ANTHROPIC_API_KEY not set - will use simulated responses"
    echo "   To use real AI integration:"
    echo "   1. Get an API key from https://console.anthropic.com/"
    echo "   2. Run: export ANTHROPIC_API_KEY=your_key_here"
    echo "   3. Re-run this script"
else
    echo "✅ ANTHROPIC_API_KEY found - will use real AI integration"
fi

echo
echo "🚀 Starting SwarmRouter Minimal MVP Demo..."
echo

# Run the demo
python3 minimal_mcp_server.py --demo

echo
echo "✨ Demo completed!"
echo
echo "📖 Next steps:"
echo "   • Read README_MINIMAL_MVP.md for detailed documentation"
echo "   • Try: python3 examples.py for more usage examples"
echo "   • Run: python3 test_minimal.py to verify everything works"
echo "   • Use: python3 minimal_mcp_server.py --server for MCP mode"
echo
echo "🐝 Keep It Simple, Swarmers!"