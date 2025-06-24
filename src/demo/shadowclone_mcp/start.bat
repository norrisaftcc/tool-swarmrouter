@echo off
rem Shadow Clone MCP Demo Startup Script (Windows)
rem Starts the shadow clone ninja demonstration

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo 🥷 Shadow Clone MCP Demo Startup
echo =================================

rem Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ and try again.
    echo    Download from: https://nodejs.org/
    pause
    exit /b 1
)

rem Get Node.js version
for /f "tokens=1 delims=v" %%a in ('node --version') do set NODE_VERSION=%%a

echo ✅ Node.js version: %NODE_VERSION%

rem Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    call npm install
    if !errorlevel! neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)

echo.
echo 🎌 Choose your shadow clone experience:
echo 1^) 🎮 Interactive Demo ^(watch ninjas in action^)
echo 2^) 🔧 MCP Server ^(connect to Claude Desktop^)
echo 3^) 🧪 Run Tests
echo.

set /p choice="Select option (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting Interactive Shadow Clone Demo...
    echo    Watch as ninjas create shadow clones for different missions!
    echo.
    node examples/ninja_demo.js
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Starting MCP Server...
    echo    Configure Claude Desktop with the provided config file.
    echo    Server will run until you press Ctrl+C
    echo.
    echo 📋 Claude Desktop Config:
    echo    Add this to your Claude Desktop configuration:
    echo.
    type claude_desktop_config.json
    echo.
    echo    Update the 'cwd' path to: %CD%
    echo.
    pause
    node server.js
) else if "%choice%"=="3" (
    echo.
    echo 🧪 Running Shadow Clone Tests...
    call npm test
) else (
    echo ❌ Invalid option. Please choose 1, 2, or 3.
    pause
    exit /b 1
)

echo.
echo 🎉 Shadow Clone demo completed!
echo 💡 Learn more about SwarmRouter at: https://github.com/norrisaftcc/tool-swarmrouter
pause