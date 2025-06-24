# Shadow Clone MCP Server Testing Guide

## Overview

This guide documents how to test the Shadow Clone MCP server and provides a model for students to understand MCP server testing, JSON-RPC communication, and AI agent system validation.

## Prerequisites

Before testing, ensure you have:

1. **Environment Setup**:
   ```bash
   # Navigate to the Shadow Clone directory
   cd src/demo/shadowclone_mcp
   
   # Verify Node.js dependencies are installed
   npm list @modelcontextprotocol/sdk
   ```

2. **Environment Variables** (optional, for full integration):
   ```bash
   # Copy and configure environment file
   cp ../../../.env.example ../../../.env
   # Edit .env with your API keys if testing with external services
   ```

## Testing Methods

### Method 1: Basic Server Startup Test

**Purpose**: Verify the server starts without errors and displays the welcome message.

```bash
# Test basic server startup
echo '{}' | node server.js 2>&1 | head -10
```

**Expected Output**:
```
🥷 Shadow Clone MCP Server running and ready for missions!
🎓 Perfect for learning task delegation and parallel processing concepts.
```

**Learning Objective**: Understanding MCP server initialization and stdio transport.

### Method 2: Tool Discovery Test

**Purpose**: Verify all ninja tools are properly registered and discoverable.

```bash
# Test MCP tools/list endpoint
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node server.js 2>/dev/null | jq '.result.tools[].name'
```

**Expected Output**:
```
"create_shadow_clones"
"code_review_ninja"
"debug_ninja"
"research_ninja"
"refactor_ninja"
"testing_ninja"
"architect_ninja"
"task_planner_ninja"
"sensei_status"
```

**Learning Objective**: Understanding JSON-RPC protocol and MCP tool registration.

### Method 3: Status Check Test

**Purpose**: Test basic tool execution and status reporting.

```bash
# Test sensei status tool
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sensei_status", "arguments": {}}}' | node server.js 2>/dev/null | jq '.result.content[0].text'
```

**Expected Output** (formatted):
```
🥷 Coding Sensei Status Report

👨‍🏫 Sensei: Master Sensei
🎯 Specialization: Full-Stack Development
📊 Experience: Expert
🎌 Focus: Educational Coding

👥 Active Clones: 0
✅ Completed Missions: 0

📈 Clone Status Breakdown:
• Created: 0
• Executing: 0
• Completed: 0
• Failed: 0

🎓 Educational Note: This demonstrates efficient task delegation and parallel processing!
```

**Learning Objective**: Understanding tool execution, parameter passing, and response formatting.

### Method 4: Shadow Clone Creation Test

**Purpose**: Test the core functionality - task delegation and parallel processing.

```bash
# Test shadow clone creation with a simple educational task
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "create_shadow_clones", "arguments": {"mission": "Explain the concept of recursion in programming", "maxTokens": 500}}}' | node server.js 2>/dev/null
```

**Expected Behavior**:
1. Server logs show mission analysis and clone creation
2. Multiple clones execute in parallel
3. Token efficiency statistics are calculated
4. Response includes mission summary and results

**Key Metrics to Verify**:
- **Token Efficiency**: Should show 60-80% savings
- **Clone Count**: Should create 2-4 clones based on task complexity
- **Success Rate**: All clones should complete successfully
- **Execution Time**: Should complete within 2-3 seconds

**Learning Objective**: Understanding distributed task execution and efficiency measurement.

### Method 5: Specialized Ninja Test

**Purpose**: Test specialized ninja tools for educational scenarios.

```bash
# Test code review ninja
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "code_review_ninja", "arguments": {"code": "function fibonacci(n) { if (n <= 1) return n; return fibonacci(n-1) + fibonacci(n-2); }", "language": "javascript", "focus": "performance"}}}' | node server.js 2>/dev/null | jq '.result.content[0].text'
```

**Expected Output**: Detailed code review with performance recommendations, security considerations, and educational insights.

**Learning Objective**: Understanding specialized AI agents and domain-specific analysis.

## Comprehensive Test Script

Create a test script for automated validation:

```bash
#!/bin/bash
# shadow_clone_test.sh

echo "🧪 Starting Shadow Clone MCP Server Tests..."

# Test 1: Server Startup
echo "Test 1: Server Startup"
if echo '{}' | timeout 5s node server.js 2>&1 | grep -q "Shadow Clone MCP Server running"; then
    echo "✅ Server starts successfully"
else
    echo "❌ Server startup failed"
    exit 1
fi

# Test 2: Tool Discovery
echo "Test 2: Tool Discovery"
TOOL_COUNT=$(echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node server.js 2>/dev/null | jq '.result.tools | length')
if [ "$TOOL_COUNT" -eq 9 ]; then
    echo "✅ All 9 tools discovered"
else
    echo "❌ Expected 9 tools, found $TOOL_COUNT"
    exit 1
fi

# Test 3: Basic Tool Execution
echo "Test 3: Basic Tool Execution"
if echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sensei_status", "arguments": {}}}' | node server.js 2>/dev/null | jq -e '.result.content[0].text' > /dev/null; then
    echo "✅ Tool execution successful"
else
    echo "❌ Tool execution failed"
    exit 1
fi

# Test 4: Shadow Clone Creation
echo "Test 4: Shadow Clone Creation"
RESPONSE=$(echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "create_shadow_clones", "arguments": {"mission": "Test mission", "maxTokens": 300}}}' | node server.js 2>/dev/null)
if echo "$RESPONSE" | jq -e '.result.content[0].text' | grep -q "Token Efficiency"; then
    echo "✅ Shadow clone creation successful"
else
    echo "❌ Shadow clone creation failed"
    exit 1
fi

echo "🎉 All tests passed! Shadow Clone MCP Server is ready for educational use."
```

## Student Learning Exercises

### Exercise 1: Understanding JSON-RPC
**Objective**: Learn MCP communication protocol

1. Manually construct a JSON-RPC request
2. Identify required fields: `jsonrpc`, `id`, `method`, `params`
3. Test with different tool names and observe responses

### Exercise 2: Token Efficiency Analysis
**Objective**: Understand distributed processing benefits

1. Run the same task with different `maxTokens` values
2. Compare efficiency percentages
3. Analyze how task complexity affects clone count

### Exercise 3: Error Handling
**Objective**: Learn robust system design

1. Test with invalid tool names
2. Test with missing required parameters
3. Observe error responses and learn from them

### Exercise 4: Specialized Tool Comparison
**Objective**: Understand domain-specific AI agents

1. Test each ninja tool with appropriate inputs
2. Compare response styles and focus areas
3. Identify when to use each specialization

## Troubleshooting

### Common Issues

1. **"SyntaxError: The requested module does not provide an export"**
   - Check that all imports match actual exports
   - Verify MCP SDK version compatibility

2. **"Cannot find module" errors**
   - Ensure `npm install` was run in the correct directory
   - Check package.json dependencies

3. **JSON parsing errors**
   - Validate JSON syntax with `jq` or online validator
   - Ensure proper escaping of quotes in parameters

4. **Server hangs or timeouts**
   - Use `timeout` command to limit test duration
   - Check for infinite loops in clone execution

### Debugging Tips

1. **Enable verbose logging**:
   ```bash
   DEBUG=* node server.js
   ```

2. **Test individual components**:
   ```bash
   # Test just the ninja classes
   node -e "import('./lib/ninja.js').then(m => console.log(Object.keys(m)))"
   ```

3. **Validate JSON responses**:
   ```bash
   echo 'request' | node server.js 2>/dev/null | jq '.'
   ```

## Integration with Claude Code

When using this server with Claude Code or other MCP clients:

1. **Configuration**: Add to `.mcp.json` or MCP client config
2. **Environment**: Ensure environment variables are set
3. **Testing**: Use MCP client's built-in testing tools
4. **Monitoring**: Watch server logs for debugging

## Educational Value

This testing process teaches:

- **MCP Protocol**: JSON-RPC communication patterns
- **Distributed Systems**: Task delegation and parallel processing
- **Error Handling**: Robust system design principles
- **Performance Measurement**: Token efficiency and optimization
- **API Design**: Tool interfaces and parameter validation
- **Testing Methodologies**: Automated testing and validation

Perfect for computer science students learning about:
- Distributed computing concepts
- AI agent systems
- API development and testing
- System integration
- Performance optimization

## Next Steps

After successful testing:

1. **Integration Testing**: Test with Task Master AI for complete workflow
2. **Load Testing**: Test with multiple concurrent requests
3. **Performance Profiling**: Analyze token usage patterns
4. **Educational Deployment**: Set up for classroom use
5. **Documentation**: Create student tutorials and exercises

---

*This testing guide serves as both validation documentation and educational material for understanding MCP server development and AI agent system testing.*