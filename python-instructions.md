# Python Coding Instructions

## Project Overview

This document provides comprehensive coding standards and best practices for Python development. These guidelines ensure code consistency, maintainability, and adherence to Python community standards across all Python-based projects.

## Code Formatting Standards

### Required Tools
- **black**: Uncompromising Python code formatter
- **isort**: Import statement organizer with black compatibility
- **flake8**: Code linting and style checking

### Configuration
Set up your development environment with these commands:
```bash
# Format code with black (88-character line length)
black --line-length 88 .

# Organize imports with isort
isort --profile black .

# Lint code with flake8
flake8 --max-line-length 88 --extend-ignore E203,W503 .
```

### IDE Configuration
Configure your IDE/editor to:
- Use black formatting on save
- Sort imports automatically with isort
- Show flake8 warnings inline
- Use 4 spaces for indentation (never tabs)

## GitHub Copilot Setup Workflow

For projects using GitHub Copilot, you can automate the development environment setup with a workflow file. Create `.github/workflows/copilot-setup-steps.yml`:

```yaml
name: "Copilot Setup Steps"

# Automatically run setup steps for validation and manual testing
on:
  workflow_dispatch:
  push:
    paths:
      - .github/workflows/copilot-setup-steps.yml
  pull_request:
    paths:
      - .github/workflows/copilot-setup-steps.yml

jobs:
  # The job MUST be called 'copilot-setup-steps'
  copilot-setup-steps:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          cache: "pip"
      
      - name: Create virtual environment
        run: python -m venv venv
      
      - name: Activate virtual environment and install dependencies
        run: |
          source venv/bin/activate
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Verify installation
        run: |
          source venv/bin/activate
          python --version
          pip list
          
      - name: Run basic checks
        run: |
          source venv/bin/activate
          black --check . || echo "Code formatting needed"
          flake8 . || echo "Linting issues found"
          pytest --collect-only || echo "Test discovery completed"
```

This workflow ensures that:
- Virtual environment is created correctly
- All dependencies install without conflicts
- Basic code quality checks can run
- The development environment is ready for Copilot assistance

## Development Workflow

### Environment Setup

#### 1. Python Version Requirements
Use Python 3.9+ (recommend latest stable version). Check your Python version:
```bash
python --version
# or
python3 --version
```

#### 2. Virtual Environment Setup (CRITICAL)

**Why Virtual Environments?** Virtual environments isolate your project's dependencies from your system Python installation. This prevents version conflicts between different projects and keeps your system clean.

##### Step-by-Step Virtual Environment Creation:

**For Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (you should see (venv) in your prompt)
where python
# Should show path to venv\Scripts\python.exe
```

**For macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
which python
# Should show path to venv/bin/python
```

##### Common Virtual Environment Issues and Solutions:

**Problem: "python: command not found"**
- Windows: Use `python` or `py`
- macOS/Linux: Use `python3`

**Problem: Virtual environment won't activate**
- Windows: Try `venv\Scripts\activate.bat` or use PowerShell: `venv\Scripts\Activate.ps1`
- macOS/Linux: Ensure you have `source` before the path

**Problem: Still using system Python after activation**
- Deactivate with `deactivate` and try again
- Check that you see `(venv)` in your terminal prompt

#### 3. Dependency Installation

Always install dependencies AFTER activating your virtual environment:

```bash
# First, ensure virtual environment is activated
# You should see (venv) in your prompt

# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies (linting, testing tools)
pip install -r requirements-dev.txt

# Verify installations
pip list
```

#### 4. Working with requirements.txt

**Creating requirements.txt:**
```bash
# Generate requirements from current environment
pip freeze > requirements.txt

# For development dependencies
pip freeze > requirements-dev.txt
```

**Sample requirements.txt structure:**
```txt
# Core dependencies
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
requests==2.31.0

# Database
sqlalchemy==2.0.23
alembic==1.13.1

# Utilities
python-dotenv==1.0.0
```

**Sample requirements-dev.txt:**
```txt
# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1

# Code quality
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1

# Development tools
pre-commit==3.6.0
```

#### 5. Daily Workflow Checklist

Every time you start working on the project:

1. **Navigate to project directory**
   ```bash
   cd /path/to/your/project
   ```

2. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Verify activation**
   - Look for `(venv)` in your terminal prompt
   - Run `pip list` to see installed packages

4. **When finished, deactivate**
   ```bash
   deactivate
   ```

### Development Commands
```bash
# Format and organize code
black src/ tests/
isort src/ tests/

# Check formatting (CI pipeline)
black --check src/ tests/
isort --check-only src/ tests/

# Lint code
flake8 src/ tests/

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Type checking (if using mypy)
mypy src/
```

## Repository Structure

```
project-name/
├── src/
│   └── project_name/        # Main package (use underscores)
│       ├── __init__.py
│       ├── main.py          # Entry point
│       ├── models/          # Data models (Pydantic, dataclasses)
│       ├── services/        # Business logic
│       ├── utils/           # Utility functions
│       └── config/          # Configuration management
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   ├── conftest.py        # Pytest configuration
│   └── fixtures/          # Test data and fixtures
├── docs/                   # Documentation
├── scripts/               # Utility scripts
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── pyproject.toml        # Python project configuration
├── .gitignore            # Git ignore patterns
└── README.md             # Project documentation
```

## Development Guidelines

### Python Code Style
- Follow **PEP 8** standards strictly
- Use **type hints** for all function signatures, class attributes, and variables
- Write descriptive variable and function names using `snake_case`
- Use `CapitalCase` for class names
- Keep functions focused and under 20 lines when possible
- Prefer explicit over implicit code

### Type Hints and Documentation
```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

def process_data(items: List[str], max_items: Optional[int] = None) -> Dict[str, Any]:
    """Process a list of items and return summary statistics.
    
    Args:
        items: List of string items to process
        max_items: Maximum number of items to process (None for no limit)
        
    Returns:
        Dictionary containing processing results and statistics
        
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    
    # Implementation here
    return {"count": len(items), "processed": True}
```

### Error Handling
- Use specific exception types, not bare `except:`
- Implement proper logging for errors
- Use context managers (`with` statements) for resource management
- Fail fast with clear error messages

### Data Models
- Use **Pydantic** for API data validation and serialization
- Use **dataclasses** for simple data containers
- Implement proper `__str__` and `__repr__` methods

```python
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional

class UserRequest(BaseModel):
    """API request model for user data."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)

@dataclass
class ProcessingResult:
    """Internal data structure for processing results."""
    success: bool
    message: str
    data: Optional[dict] = None
```

## Testing Strategy

### Testing Framework
- Use **pytest** as the primary testing framework
- Organize tests to mirror source code structure
- Use descriptive test function names

### Test Categories
```python
# Unit tests - test individual functions/classes
def test_user_validation_success():
    """Test successful user data validation."""
    user = UserRequest(name="John Doe", email="john@example.com", age=30)
    assert user.name == "John Doe"

# Integration tests - test component interactions
def test_api_endpoint_integration():
    """Test complete API endpoint workflow."""
    # Test full request/response cycle

# Fixtures for reusable test data
@pytest.fixture
def sample_user():
    """Provide sample user data for tests."""
    return {"name": "Test User", "email": "test@example.com"}
```

### Test Coverage
- Maintain >80% test coverage for core business logic
- Test both happy path and error conditions
- Use mocking for external dependencies

## Configuration Management

### Environment Variables
```python
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application configuration using environment variables."""
    debug: bool = False
    database_url: str
    api_key: str
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

# Usage
settings = Settings()
```

### Configuration Files
- Use `.env` files for local development
- Provide `.env.example` with all required variables
- Never commit secrets to version control
- Validate configuration at application startup

## Logging

### Structured Logging
```python
import logging
import json
from typing import Dict, Any

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_structured(level: str, message: str, extra_data: Optional[Dict[str, Any]] = None):
    """Log structured data in JSON format."""
    log_data = {
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        **(extra_data or {})
    }
    getattr(logger, level.lower())(json.dumps(log_data))
```

## Package Management

### Dependencies
- Pin exact versions in `requirements.txt` for production
- Use `requirements-dev.txt` for development tools
- Regular dependency updates and security audits
- Use `pip-tools` for dependency management

### Project Configuration
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your-project"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.9"

[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
```

## Student Quick Start Guide

### First Time Setup (Do Once)

1. **Check Python Installation**
   ```bash
   python --version
   # Should show Python 3.9 or higher
   ```

2. **Clone/Download Project**
   ```bash
   git clone <repository-url>
   cd <project-name>
   ```

3. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   
   # macOS/Linux  
   python3 -m venv venv
   ```

4. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

5. **Install Dependencies**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

### Every Time You Work (Daily Routine)

1. **Open terminal in project directory**
2. **Activate virtual environment**
   ```bash
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```
3. **Verify activation** - Look for `(venv)` in prompt
4. **Start coding!**
5. **When done:** `deactivate`

### Emergency Troubleshooting

**"Nothing works!" Recovery Steps:**
1. Delete `venv` folder completely
2. Create new virtual environment: `python -m venv venv`
3. Activate it (see commands above)
4. Reinstall everything: `pip install -r requirements.txt`

**"I can't activate the virtual environment"**
- Windows users: Try PowerShell instead of Command Prompt
- Make sure you're in the project directory
- Check that `venv` folder exists

**"Packages not found after installation"**
- Check that virtual environment is activated (look for `(venv)`)
- Try `pip list` to see what's installed
- Reinstall with `pip install -r requirements.txt`

## Best Practices Summary

1. **Always use type hints** - improves code clarity and IDE support
2. **Write comprehensive docstrings** - document purpose, parameters, and return values
3. **Keep functions small** - single responsibility principle
4. **Use meaningful names** - code should be self-documenting
5. **Handle errors gracefully** - specific exceptions with clear messages
6. **Test thoroughly** - unit tests for logic, integration tests for workflows
7. **Format consistently** - use black and isort automatically
8. **Document configuration** - all environment variables and settings
9. **Use virtual environments** - isolate project dependencies
10. **Follow PEP standards** - stay consistent with Python community practices