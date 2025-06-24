#!/bin/bash
# SwarmRouter MCP Server - Quick Start Script
# This script sets up the environment and starts the MCP server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🐝 SwarmRouter:${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# ASCII Art Header
echo -e "${YELLOW}"
cat << "EOF"
   ___                           ___       _            
  / __\_      ____ _ _ __ _ __   / _ \ ___ | |_ ___ _ __ 
 / _\ \ \ /\ / / _` | '__| '_ \ / /_)/ _ \| __/ _ \ '__|
/ /    \ V  V / (_| | |  | | | / ___/ (_) | ||  __/ |   
\/      \_/\_/ \__,_|_|  |_| |_\/    \___/ \__\___|_|   
                                                        
EOF
echo -e "${NC}"

print_status "Starting SwarmRouter MCP Server setup..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found. Please run this script from the swarmrouter-mcp directory."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed."
    exit 1
fi

print_status "Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt --quiet
print_success "Dependencies installed"

# Check for .env file
if [ ! -f ".env" ]; then
    print_warning ".env file not found"
    print_status "Copying .env.example to .env..."
    cp .env.example .env
    print_warning "Please edit .env file and add your API keys before using the server"
    echo ""
    echo -e "${YELLOW}Required environment variables:${NC}"
    echo "  ANTHROPIC_API_KEY=your_api_key_here"
    echo ""
else
    print_success ".env file found"
fi

# Run tests to make sure everything works
print_status "Running tests..."
if python -m pytest tests/ --quiet --tb=short; then
    print_success "All tests passed!"
else
    print_warning "Some tests failed, but server may still work"
fi

# Show available commands
echo ""
echo -e "${GREEN}🎉 Setup complete! Here are your options:${NC}"
echo ""
echo -e "${BLUE}Start the MCP server:${NC}"
echo "  ./start.sh server"
echo ""
echo -e "${BLUE}Run the queen bee example:${NC}"
echo "  ./start.sh queen-bee"
echo ""
echo -e "${BLUE}Run tests:${NC}"
echo "  ./start.sh test"
echo ""
echo -e "${BLUE}Run development tools:${NC}"
echo "  ./start.sh lint    # Code linting"
echo "  ./start.sh format  # Code formatting"
echo "  ./start.sh type    # Type checking"
echo ""

# Handle command line arguments
case "${1:-}" in
    "server"|"mcp")
        print_status "Starting MCP server..."
        if [ ! -f ".env" ] || ! grep -q "ANTHROPIC_API_KEY=" .env; then
            print_warning "No API key found. Running in demo mode..."
            python -m src.server
        else
            print_status "Starting with MCP protocol support..."
            mcp dev src/server.py
        fi
        ;;
    "queen-bee"|"demo")
        print_status "Running queen bee coordination example..."
        if [ ! -f ".env" ] || ! grep -q "ANTHROPIC_API_KEY=" .env; then
            print_error "API key required for queen bee example. Please set ANTHROPIC_API_KEY in .env file."
            exit 1
        fi
        python examples/queen_bee_example.py
        ;;
    "test")
        print_status "Running test suite..."
        python -m pytest tests/ -v --cov=src --cov-report=term-missing
        ;;
    "lint")
        print_status "Running linter..."
        ruff check src/ tests/ examples/
        ;;
    "format")
        print_status "Formatting code..."
        black src/ tests/ examples/
        print_success "Code formatted"
        ;;
    "type")
        print_status "Running type checker..."
        mypy src/
        ;;
    "clean")
        print_status "Cleaning up..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -name "*.pyc" -delete 2>/dev/null || true
        print_success "Cleanup complete"
        ;;
    "help"|"-h"|"--help")
        echo "Usage: ./start.sh [command]"
        echo ""
        echo "Commands:"
        echo "  server     Start the MCP server"
        echo "  queen-bee  Run the queen bee coordination example"
        echo "  test       Run the test suite"
        echo "  lint       Check code with linter"
        echo "  format     Format code with Black"
        echo "  type       Run type checker"
        echo "  clean      Clean up Python cache files"
        echo "  help       Show this help message"
        ;;
    "")
        # Default case - just setup, show help
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Run './start.sh help' for available commands"
        exit 1
        ;;
esac