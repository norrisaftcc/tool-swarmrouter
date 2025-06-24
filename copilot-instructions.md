# Copilot Instructions for SwarmRouter

## Project Overview

SwarmRouter (internally known as "waggle") is a Python-based FastAPI routing proxy for Large Language Models (LLMs). This project focuses on building a prototype that can intelligently route requests across multiple LLM endpoints while maintaining simplicity and extensibility. The core philosophy is "Keep It Simple Swarmers" - waggle should remain lightweight and focused.

## Project Architecture

This is a FastAPI-based web service designed to:
- Route LLM requests to appropriate backend services
- Provide load balancing and failover capabilities
- Maintain request/response logging and metrics
- Support multiple LLM providers and endpoints

## Code Formatting Standards

### Required Tools
- **black**: Code formatter with line length of 88 characters
- **isort**: Import statement organizer with black compatibility
- **flake8**: Linting for code quality (optional but recommended)

### Configuration
Ensure your development environment uses:
```bash
black --line-length 88 .
isort --profile black .
flake8 --max-line-length 88 --extend-ignore E203,W503
```

## Development Workflow

### Getting Started
1. Clone the repository
2. Set up a Python virtual environment (Python 3.9+ recommended)
3. Install dependencies: `pip install -r requirements.txt`
4. Install development dependencies: `pip install -r requirements-dev.txt`

### Running the Service
```bash
# Development server with auto-reload
uvicorn src.prototype.main:app --reload --host 0.0.0.0 --port 8000

# Production-like server
uvicorn src.prototype.main:app --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/prototype --cov-report=html

# Run specific test categories
pytest tests/unit/        # Unit tests
pytest tests/integration/ # Integration tests
```

### Linting and Code Quality
```bash
# Format code
black src/ tests/
isort src/ tests/

# Check formatting (CI pipeline)
black --check src/ tests/
isort --check-only src/ tests/

# Lint code
flake8 src/ tests/
```

### Health Checks
```bash
# Quick development check
make dev-check  # or run: black . && isort . && flake8 . && pytest

# Full CI pipeline check
make ci-check
```

## Repository Structure

```
tool-swarmrouter/
├── src/
│   └── prototype/          # Main application code (waggle core)
│       ├── main.py         # FastAPI application entry point
│       ├── routers/        # API route handlers
│       ├── services/       # Business logic and LLM integrations
│       ├── models/         # Pydantic models and schemas
│       ├── utils/          # Utility functions and helpers
│       └── config/         # Configuration management
├── tests/
│   ├── unit/              # Unit tests for individual components
│   ├── integration/       # Integration tests for API endpoints
│   └── fixtures/          # Test data and fixtures
├── docs/                  # Documentation and API specs
├── logs/                  # Application logs (local development)
├── scripts/               # Deployment and utility scripts
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── pyproject.toml        # Python project configuration
├── Dockerfile            # Container configuration
└── docker-compose.yml    # Local development environment
```

## Development Guidelines

### Python Code Style
- Write **idiomatic Python** following PEP 8 standards
- Use type hints for all function signatures and class attributes
- Prefer composition over inheritance
- Use descriptive variable and function names
- Keep functions focused and single-purpose

### API Design
- Design **clear API signatures** with explicit request/response models
- Use Pydantic models for data validation and serialization
- Follow RESTful conventions where appropriate
- Version your APIs (`/v1/`, `/v2/`) for future compatibility
- Provide comprehensive OpenAPI documentation via FastAPI

### Documentation
- Write **comprehensive docstrings** for all public functions and classes
- Use Google-style docstrings for consistency
- Include type information and examples in docstrings
- Keep README.md updated with setup and usage instructions
- Document API endpoints and their expected behavior

### Logging and Monitoring
- Implement **structured logging** using Python's logging module
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Log request/response data for LLM interactions (with privacy considerations)
- Include correlation IDs for request tracing
- Log performance metrics and routing decisions

### Extensibility and Architecture
- Design for **extensibility** - new LLM providers should be easy to add
- Use dependency injection patterns for service configuration
- Implement abstract base classes for LLM providers
- Support plugin-style architecture for custom routing logic
- Maintain backward compatibility when possible

### Testing Strategy
- Write **unit tests for routing logic** and business logic components
- Test LLM provider integrations with mocked responses
- Include integration tests for complete request/response cycles
- Test error handling and edge cases
- Maintain >80% test coverage for core routing logic

### Configuration Management
- Use environment variables for runtime configuration
- Provide sensible defaults for development
- Support multiple configuration profiles (dev, staging, prod)
- Validate configuration at startup
- Document all configuration options

## Waggle-Specific Notes

When working on this project (internally waggle), keep in mind:
- The routing algorithms are the heart of waggle's intelligence
- Performance and latency are critical for LLM routing
- The service should gracefully handle LLM provider failures
- Waggle should support both synchronous and asynchronous routing
- Consider rate limiting and quota management for different LLM providers

## Documentation Updates

When making changes:
- Update API documentation in `docs/` directory
- Refresh OpenAPI specs if endpoints change
- Update this copilot-instructions.md if development practices evolve
- Keep deployment documentation current
- Document any new environment variables or configuration options

## Getting Help

- Check existing issues and documentation first
- For waggle-specific questions, reference the internal architecture docs
- Follow the established patterns in the codebase
- When in doubt, prioritize simplicity and maintainability