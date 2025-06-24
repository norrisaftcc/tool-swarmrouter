#!/bin/bash

# Shadow Clone MCP Demo Startup Script
# Starts the shadow clone ninja demonstration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🥷 Shadow Clone MCP Demo Startup"
echo "================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2)
REQUIRED_VERSION="18.0.0"

if ! npx semver -r ">=$REQUIRED_VERSION" "$NODE_VERSION" &> /dev/null; then
    echo "❌ Node.js version $NODE_VERSION is too old. Please upgrade to Node.js 18+ and try again."
    exit 1
fi

echo "✅ Node.js version: $NODE_VERSION"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🎌 Choose your shadow clone experience:"
echo "1) 🎮 Interactive Demo (watch ninjas in action)"
echo "2) 🔧 MCP Server (connect to Claude Desktop)"
echo "3) 🧪 Run Tests"
echo ""

read -p "Select option (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Interactive Shadow Clone Demo..."
        echo "   Watch as ninjas create shadow clones for different missions!"
        echo ""
        node examples/ninja_demo.js
        ;;
    2)
        echo ""
        echo "🔧 Starting MCP Server..."
        echo "   Configure Claude Desktop with the provided config file."
        echo "   Server will run until you press Ctrl+C"
        echo ""
        echo "📋 Claude Desktop Config:"
        echo "   Add this to your Claude Desktop configuration:"
        echo ""
        cat claude_desktop_config.json
        echo ""
        echo "   Update the 'cwd' path to: $SCRIPT_DIR"
        echo ""
        read -p "Press Enter to start server..."
        node server.js
        ;;
    3)
        echo ""
        echo "🧪 Running Shadow Clone Tests..."
        npm test
        ;;
    *)
        echo "❌ Invalid option. Please choose 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "🎉 Shadow Clone demo completed!"
echo "💡 Learn more about SwarmRouter at: https://github.com/norrisaftcc/tool-swarmrouter"