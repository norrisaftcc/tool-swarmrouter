# SwarmRouter (Waggle) - Initial Project Setup

**Note: This is an initial scaffolding setup for the MVP. Code is not yet fully functional.**

SwarmRouter is an intelligent AI model routing system that distributes requests between local inference servers and cloud providers, optimizing for performance, cost, and availability. The system operates under the code name "waggle" for internal development references.

## Architecture Overview

The system follows a lightweight, microservices-inspired architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    SwarmRouter (Waggle)                     │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Application (main.py)                             │
│  ├─ /v1/chat/completions (OpenAI-compatible endpoint)      │
│  ├─ /admin/overflow_provider (configuration endpoint)      │
│  └─ /health (monitoring endpoint)                          │
├─────────────────────────────────────────────────────────────┤
│  Router Engine (router.py)                                 │
│  ├─ Provider Selection Logic                               │
│  ├─ Load Balancing & Failover                             │
│  └─ Request/Response Orchestration                         │
├─────────────────────────────────────────────────────────────┤
│  Provider Adapters (adapters.py)                           │
│  ├─ LMStudioAdapter (Local Inference)                     │
│  ├─ OpenRouterAdapter (Cloud Routing)                     │
│  └─ AzureAdapter (Enterprise Cloud)                       │
├─────────────────────────────────────────────────────────────┤
│  Configuration Management (config.py)                      │
│  └─ Environment-based configuration with validation        │
└─────────────────────────────────────────────────────────────┘
```

## MVP Goals

The MVP focuses on establishing a solid foundation for the routing system:

### Primary Objectives
- **Local-First Routing**: Prioritize local LM Studio instances for fast, private inference
- **Intelligent Overflow**: Seamlessly fall back to cloud providers (OpenRouter, Azure) when local resources are unavailable
- **OpenAI Compatibility**: Maintain full compatibility with OpenAI's chat completions API
- **Simple Administration**: Provide basic endpoints for runtime configuration management
- **Monitoring Foundation**: Establish health checking and basic metrics collection

### MVP Routing Strategy
1. **Local Provider Priority**: Try LM Studio first for all requests
2. **Smart Failover**: Route to cloud providers if local fails or is unavailable
3. **Simple Load Distribution**: Basic round-robin between available overflow providers
4. **Health-Aware Routing**: Skip providers marked as unhealthy

## Configuration

The system uses environment variables for configuration:

### Local Provider (LM Studio)
```bash
LMSTUDIO_ENABLED=true
LMSTUDIO_URL=http://localhost:1234
LMSTUDIO_TIMEOUT=30
```

### Cloud Providers
```bash
# OpenRouter
OPENROUTER_ENABLED=true
OPENROUTER_API_KEY=your_key_here

# Azure OpenAI
AZURE_ENABLED=false
AZURE_ENDPOINT=https://your-resource.openai.azure.com
AZURE_API_KEY=your_key_here
```

### System Configuration
```bash
SWARMROUTER_OVERFLOW_TIMEOUT=60
SWARMROUTER_MAX_RETRIES=3
SWARMROUTER_LOG_LEVEL=INFO
```

## Getting Started (MVP)

### 1. Environment Setup
```bash
cd src/prototype
pip install -r requirements.txt
```

### 2. Configuration
Copy `.env.example` to `.env` and configure your providers:
```bash
cp .env.example .env
# Edit .env with your provider configurations
```

### 3. Run the Service
```bash
python main.py
```

The service will start on `http://localhost:8000` with the following endpoints:

- `POST /v1/chat/completions` - OpenAI-compatible chat endpoint
- `GET /health` - Service health check
- `POST /admin/overflow_provider` - Runtime provider configuration
- `GET /admin/status` - Detailed system status

## API Usage

### Chat Completions
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello, world!"}
    ]
  }'
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Provider Configuration
```bash
curl -X POST http://localhost:8000/admin/overflow_provider \
  -H "Content-Type: application/json" \
  -d '{
    "type": "openrouter",
    "api_key": "your_new_key_here"
  }'
```

## Stretch Goals (Future Iterations)

### Advanced Routing
- **Model-Aware Routing**: Route requests based on specific model capabilities and availability
- **Cost Optimization**: Factor in provider costs for intelligent routing decisions
- **Geographic Routing**: Route to geographically closer providers for reduced latency
- **Request Caching**: Cache responses for identical requests to improve performance

### Performance & Scalability
- **Streaming Support**: Implement streaming responses for real-time applications
- **Request Batching**: Batch multiple requests for improved provider utilization
- **Connection Pooling**: Optimize HTTP connections to providers
- **Horizontal Scaling**: Support multiple SwarmRouter instances with shared state

### Monitoring & Analytics
- **Comprehensive Metrics**: Detailed performance, cost, and usage analytics
- **Distributed Tracing**: Full request lifecycle tracing across providers
- **Alerting System**: Proactive notifications for system health issues
- **Usage Analytics**: Detailed insights into routing patterns and optimization opportunities

### Enterprise Features
- **Authentication & Authorization**: Secure API access with role-based permissions
- **Rate Limiting**: Configurable rate limits per user/application
- **Audit Logging**: Comprehensive logging for compliance and debugging
- **Multi-Tenancy**: Support for multiple isolated environments

## Development Workflow

### MVP Phase (Current)
1. **Scaffolding** ✓ - Basic project structure and API endpoints
2. **Core Routing** - Implement basic local-first routing logic
3. **Provider Integration** - Complete adapter implementations
4. **Testing** - Unit tests for core functionality
5. **Documentation** - API documentation and deployment guides

### Future Phases
- **Phase 2**: Advanced routing algorithms and caching
- **Phase 3**: Monitoring, metrics, and analytics
- **Phase 4**: Enterprise features and production hardening

## Contributing

This is an MVP project focusing on rapid prototyping and validation. Code quality standards will be established as the project matures.

### Current Focus Areas
- Core routing logic implementation
- Provider adapter completion
- Basic testing framework
- Configuration validation
- Error handling improvements

## Technical Notes

### Architecture Decisions
- **FastAPI**: Chosen for excellent async support and automatic API documentation
- **Async/Await**: Full async implementation for optimal I/O performance
- **Provider Adapters**: Abstracted provider interfaces for easy extension
- **Configuration-Driven**: Environment-based configuration for operational flexibility

### Known Limitations (MVP)
- No authentication or rate limiting
- Basic error handling without retry logic
- Limited monitoring and metrics
- No request caching or optimization
- Single-instance deployment only

### Security Considerations
- API keys stored in environment variables (not encrypted)
- No input validation beyond basic type checking
- No request/response sanitization
- Local network access required for LM Studio

---

*Project Code Name: Waggle - Keep It Simple, but Make It Smart*
