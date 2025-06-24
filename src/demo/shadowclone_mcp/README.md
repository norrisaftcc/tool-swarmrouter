# Shadow Clone MCP Server 🥷

A lightweight JavaScript MCP (Model Context Protocol) server that demonstrates efficient task delegation using the Naruto shadow clone metaphor. This server shows how complex missions can be broken down and executed by multiple "shadow clones" for improved token efficiency.

## 🎌 Concept

In the Naruto universe, shadow clones allow a ninja to create copies of themselves to tackle multiple tasks simultaneously. Our MCP server applies this concept to AI task delegation:

- **Main Ninja**: The master coordinator (like the queen bee in SwarmRouter)
- **Shadow Clones**: Task executors that handle specific subtasks
- **Jutsu Types**: Different delegation strategies based on mission complexity
- **Chakra**: Token allocation and management system

## 🔥 Jutsu Types

The server automatically selects the appropriate jutsu (technique) based on mission analysis:

| Jutsu Type | Use Case | Token Efficiency | Clone Count |
|------------|----------|------------------|-------------|
| **Multi Shadow Clone** | Complex analysis/planning | 75% savings | 3-8 clones |
| **Shadow Clone** | Standard task delegation | 65% savings | 2-4 clones |
| **Clone Network** | Information gathering | 70% savings | 2-6 clones |
| **Transform Clone** | Data transformation | 60% savings | 2 clones |
| **Dispel Clone** | Error handling/cleanup | 50% savings | 1 clone |
| **Coordination** | Result merging | 55% savings | 3 clones |

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm

### Installation

```bash
cd src/demo/shadowclone_mcp
npm install
```

### Running the Demo

```bash
# Run the interactive demo
node examples/ninja_demo.js

# Start the MCP server
npm start
# or
node server.js
```

### Running Tests

```bash
npm test
```

## 📡 MCP Server Usage

The server provides these MCP tools:

### `execute_mission`
Execute a mission using shadow clone delegation.

```json
{
  "mission": "Analyze the microservices architecture and identify optimization opportunities",
  "max_tokens": 1000,
  "priority": "high"
}
```

### `ninja_status`
Get current ninja status and active clone information.

### `mission_history`
Retrieve history of completed missions.

### `dispel_clones`
Emergency cleanup - dispel all active shadow clones.

## 🎯 Example Mission Results

```json
{
  "ninja": {
    "name": "Naruto Uzumaki",
    "village": "Hidden Leaf Village",
    "rank": "Genin",
    "stats": {
      "missionsCompleted": 1,
      "totalTokensSaved": 750,
      "averageEfficiency": 75.0,
      "clonesCreated": 4
    }
  },
  "mission": {
    "id": "mission_1703123456789",
    "result": {
      "jutsuType": "multi_shadow_clone",
      "cloneCount": 4,
      "successfulClones": 4,
      "tokenStats": {
        "allocated": 1000,
        "used": 250,
        "saved": 750,
        "efficiency": 75.0
      }
    }
  }
}
```

## 💡 Token Efficiency Demonstration

The shadow clone technique demonstrates significant token savings:

```
Traditional Approach: 1000 tokens
Shadow Clone Approach: 250 tokens used
Savings: 750 tokens (75% efficiency)
```

This efficiency comes from:
1. **Task Decomposition**: Breaking complex missions into smaller, focused subtasks
2. **Parallel Execution**: Multiple clones working simultaneously
3. **Optimized Allocation**: Each clone gets only the tokens it needs
4. **Result Coordination**: Efficient merging of clone outputs

## 🏗️ Architecture

```
src/demo/shadowclone_mcp/
├── server.js              # Main MCP server
├── lib/
│   ├── ninja.js          # Main ninja coordinator
│   ├── shadowclone.js    # Clone management
│   └── jutsu.js          # Delegation strategies
├── examples/
│   └── ninja_demo.js     # Interactive demo
├── tests/
│   └── server.test.js    # Test suite
└── README.md
```

### Key Components

- **MainNinja**: Coordinates missions and manages shadow clones
- **ShadowCloneManager**: Creates and tracks shadow clones
- **ShadowClone**: Individual clone that executes subtasks
- **Jutsu Analysis**: Determines optimal delegation strategy

## 🎮 Interactive Demo

The `ninja_demo.js` shows different types of missions:

1. **Documentation Task** → Shadow Clone Jutsu
2. **System Analysis** → Multi Shadow Clone Jutsu  
3. **Research Task** → Clone Network Jutsu
4. **Bug Fixing** → Dispel Clone Jutsu

Run it to see real-time ninja/clone coordination!

## 🧪 Testing

Comprehensive test suite covering:

- Jutsu type selection
- Clone count calculation
- Token allocation
- Mission execution
- Error handling
- Integration scenarios

```bash
npm test
```

## 🌟 Features

- **Lightweight**: Pure JavaScript, minimal dependencies
- **Educational**: Clear Naruto metaphors make concepts intuitive
- **Efficient**: Demonstrates 50-75% token savings
- **Testable**: Full test coverage with Node.js test runner
- **Observable**: Detailed logging and status reporting
- **Scalable**: Handles concurrent missions and clone management

## 🔮 Future Enhancements

- **Real LLM Integration**: Connect to actual AI models
- **Advanced Jutsu**: More sophisticated delegation patterns
- **Persistent Storage**: Mission history database
- **Performance Metrics**: Advanced analytics dashboard
- **Multi-Ninja**: Coordinate multiple ninja instances

## 🎓 Educational Value

This demo teaches:

1. **Task Delegation Patterns**: How to break down complex problems
2. **Resource Management**: Efficient token/resource allocation
3. **Parallel Processing**: Concurrent execution strategies
4. **Error Handling**: Graceful failure management
5. **Metaphorical Design**: Using familiar concepts to explain complex systems

## 📚 Comparison with SwarmRouter

| Feature | SwarmRouter (Python) | Shadow Clone (JavaScript) |
|---------|---------------------|----------------------------|
| **Metaphor** | Bee/Hive | Ninja/Shadow Clones |
| **Language** | Python | JavaScript |
| **Dependencies** | FastMCP, Pydantic | MCP SDK |
| **Deployment** | Full server setup | Single node command |
| **Use Case** | Production system | Demo/Education |
| **Complexity** | Advanced | Beginner-friendly |

## 🤝 Contributing

This is an educational project! Contributions welcome:

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

---

*🥷 "The will of fire burns bright in the Hidden Leaf Village, and so does efficient task delegation!" - Naruto Uzumaki*