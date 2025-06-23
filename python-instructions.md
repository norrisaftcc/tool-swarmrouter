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

## Development Workflow

### Environment Setup
1. Use Python 3.9+ (recommend latest stable version)
2. Always work in virtual environments:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development tools
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