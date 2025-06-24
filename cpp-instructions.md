# C++ Coding Instructions

## Project Overview

This document provides comprehensive coding standards and best practices for C++ development. These guidelines ensure code consistency, maintainability, and adherence to modern C++ standards across all C++-based projects.

## Code Formatting Standards

### Required Tools
- **clang-format**: Code formatting tool
- **clang-tidy**: Static analyzer and linter
- **cppcheck**: Static analysis tool for C/C++
- **valgrind**: Memory debugging and profiling (Linux/Mac)
- **AddressSanitizer**: Memory error detector

### Configuration
Set up your development environment with these tools:
```bash
# Format code with clang-format
clang-format -i src/**/*.cpp src/**/*.h

# Static analysis with clang-tidy
clang-tidy src/**/*.cpp -- -Iinclude

# Additional static analysis
cppcheck --enable=all --std=c++17 src/

# Memory checking (Linux/Mac)
valgrind --tool=memcheck --leak-check=full ./your_program

# AddressSanitizer (compile with -fsanitize=address)
g++ -fsanitize=address -g -o program src/main.cpp
```

### Code Style Configuration
Create `.clang-format` file in project root:
```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 100
UseTab: Never
Standard: Cpp17
AccessModifierOffset: -2
NamespaceIndentation: None
```

## Development Workflow

### Environment Setup
1. Use C++17 or C++20 (modern C++ standards)
2. Set up build system (CMake 3.15+ recommended)
3. Configure compiler with appropriate flags
4. Install development tools and dependencies

### Build System Setup

#### CMake Configuration
```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.15)

project(YourProject 
    VERSION 1.0.0
    DESCRIPTION "Your project description"
    LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra -Wpedantic")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Find packages
find_package(GTest REQUIRED)
find_package(spdlog REQUIRED)

# Include directories
include_directories(include)

# Add subdirectories
add_subdirectory(src)
add_subdirectory(tests)

# Main executable
add_executable(${PROJECT_NAME} 
    src/main.cpp
)

target_link_libraries(${PROJECT_NAME} 
    your_library
    spdlog::spdlog
)

# Enable testing
enable_testing()
```

### Development Commands
```bash
# Configure build
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..

# Build project
cmake --build .

# Run tests
ctest --output-on-failure

# Install
cmake --install . --prefix /usr/local

# Format code
find src include -name "*.cpp" -o -name "*.h" | xargs clang-format -i

# Static analysis
clang-tidy src/**/*.cpp -- -Iinclude -std=c++17
```

## Repository Structure

```
project-name/
├── src/
│   ├── main.cpp                 # Application entry point
│   ├── core/                    # Core functionality
│   │   ├── engine.cpp
│   │   └── engine.h
│   ├── utils/                   # Utility functions
│   │   ├── string_utils.cpp
│   │   └── string_utils.h
│   └── CMakeLists.txt          # Source build configuration
├── include/
│   └── project_name/           # Public headers
│       ├── api.h
│       └── types.h
├── tests/
│   ├── unit/                   # Unit tests
│   │   ├── test_engine.cpp
│   │   └── test_utils.cpp
│   ├── integration/            # Integration tests
│   └── CMakeLists.txt         # Test build configuration
├── docs/                       # Documentation
├── scripts/                    # Build and utility scripts
├── third_party/               # External dependencies
├── cmake/                     # CMake modules
├── .clang-format              # Code formatting rules
├── .clang-tidy               # Static analysis rules
├── CMakeLists.txt            # Main CMake file
├── .gitignore                # Git ignore patterns
└── README.md                 # Project documentation
```

## Development Guidelines

### Modern C++ Code Style
- Use **C++17/C++20** features when appropriate
- Follow **RAII** (Resource Acquisition Is Initialization) principle
- Use **smart pointers** instead of raw pointers
- Prefer **algorithms** over raw loops
- Use **const correctness** throughout the codebase
- Write **exception-safe** code

### Memory Management
```cpp
#include <memory>
#include <vector>
#include <string>

// Use smart pointers for dynamic allocation
class ResourceManager {
private:
    std::unique_ptr<Resource> resource_;
    std::shared_ptr<SharedResource> shared_resource_;
    
public:
    // Constructor with smart pointer initialization
    ResourceManager() 
        : resource_(std::make_unique<Resource>()),
          shared_resource_(std::make_shared<SharedResource>()) {}
    
    // Move semantics for efficiency
    ResourceManager(ResourceManager&& other) noexcept 
        : resource_(std::move(other.resource_)),
          shared_resource_(std::move(other.shared_resource_)) {}
    
    // Move assignment operator
    ResourceManager& operator=(ResourceManager&& other) noexcept {
        if (this != &other) {
            resource_ = std::move(other.resource_);
            shared_resource_ = std::move(other.shared_resource_);
        }
        return *this;
    }
    
    // Delete copy operations if not needed
    ResourceManager(const ResourceManager&) = delete;
    ResourceManager& operator=(const ResourceManager&) = delete;
};
```

### Class Design and Interface
```cpp
#pragma once

#include <string>
#include <vector>
#include <optional>

namespace project_name {

// Use enum class for type safety
enum class Status {
    kSuccess,
    kError,
    kTimeout
};

// Interface with pure virtual functions
class IDataProcessor {
public:
    virtual ~IDataProcessor() = default;
    virtual Status ProcessData(const std::vector<std::string>& input) = 0;
    virtual std::optional<std::string> GetResult() const = 0;
};

// Implementation with clear public interface
class DataProcessor : public IDataProcessor {
private:
    std::vector<std::string> processed_data_;
    mutable std::mutex data_mutex_;  // mutable for const methods
    
public:
    // Constructor with initializer list
    explicit DataProcessor(size_t initial_capacity) 
        : processed_data_{} {
        processed_data_.reserve(initial_capacity);
    }
    
    // Override interface methods
    Status ProcessData(const std::vector<std::string>& input) override;
    std::optional<std::string> GetResult() const override;
    
    // Additional public methods
    size_t GetProcessedCount() const noexcept;
    void ClearData() noexcept;
    
private:
    // Helper methods
    bool ValidateInput(const std::vector<std::string>& input) const;
    void LogProcessingStep(const std::string& step) const;
};

}  // namespace project_name
```

### Error Handling and Exceptions
```cpp
#include <stdexcept>
#include <system_error>

namespace project_name {

// Custom exception classes
class ProcessingError : public std::runtime_error {
public:
    explicit ProcessingError(const std::string& message) 
        : std::runtime_error("Processing error: " + message) {}
};

class InvalidInputError : public std::invalid_argument {
public:
    explicit InvalidInputError(const std::string& message)
        : std::invalid_argument("Invalid input: " + message) {}
};

// Function with proper error handling
std::optional<Result> ProcessFile(const std::string& filename) {
    try {
        if (filename.empty()) {
            throw InvalidInputError("Filename cannot be empty");
        }
        
        std::ifstream file(filename);
        if (!file.is_open()) {
            // Log error and return empty optional instead of throwing
            LogError("Failed to open file: " + filename);
            return std::nullopt;
        }
        
        // Processing logic here...
        return Result{/* ... */};
        
    } catch (const std::exception& e) {
        LogError("Exception in ProcessFile: " + std::string(e.what()));
        throw;  // Re-throw if unable to handle
    }
}

}  // namespace project_name
```

### Thread Safety and Concurrency
```cpp
#include <mutex>
#include <shared_mutex>
#include <atomic>
#include <thread>
#include <future>

namespace project_name {

class ThreadSafeCounter {
private:
    mutable std::shared_mutex mutex_;
    std::atomic<int> counter_{0};
    
public:
    void Increment() {
        ++counter_;  // Atomic operation, no lock needed
    }
    
    int GetValue() const {
        return counter_.load();  // Atomic read
    }
    
    // For complex operations, use locks
    void UpdateWithCalculation(int input) {
        std::unique_lock<std::shared_mutex> lock(mutex_);
        // Complex calculation requiring exclusive access
        counter_ = PerformComplexCalculation(input);
    }
    
private:
    int PerformComplexCalculation(int input) const {
        // Implementation here...
        return input * 2;
    }
};

// Async processing example
class AsyncProcessor {
public:
    std::future<Result> ProcessAsync(const Data& data) {
        return std::async(std::launch::async, [this, data]() {
            return ProcessData(data);
        });
    }
    
private:
    Result ProcessData(const Data& data) {
        // Processing implementation...
        return Result{};
    }
};

}  // namespace project_name
```

## Testing Strategy

### Testing Framework
- Use **Google Test (gtest)** as the primary testing framework
- Use **Google Mock (gmock)** for mocking dependencies
- Organize tests to mirror source code structure
- Use descriptive test names

### Test Categories
```cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "project_name/data_processor.h"

namespace project_name {
namespace test {

// Test fixture for common setup
class DataProcessorTest : public ::testing::Test {
protected:
    void SetUp() override {
        processor_ = std::make_unique<DataProcessor>(100);
    }
    
    void TearDown() override {
        processor_.reset();
    }
    
    std::unique_ptr<DataProcessor> processor_;
};

// Unit tests
TEST_F(DataProcessorTest, ProcessEmptyInputReturnsError) {
    // Arrange
    std::vector<std::string> empty_input;
    
    // Act
    Status result = processor_->ProcessData(empty_input);
    
    // Assert
    EXPECT_EQ(result, Status::kError);
}

TEST_F(DataProcessorTest, ProcessValidInputReturnsSuccess) {
    // Arrange
    std::vector<std::string> valid_input{"data1", "data2", "data3"};
    
    // Act
    Status result = processor_->ProcessData(valid_input);
    
    // Assert
    EXPECT_EQ(result, Status::kSuccess);
    EXPECT_EQ(processor_->GetProcessedCount(), 3);
}

// Parameterized tests
class DataProcessorParameterizedTest : public ::testing::TestWithParam<std::vector<std::string>> {
protected:
    DataProcessor processor_{100};
};

TEST_P(DataProcessorParameterizedTest, ProcessVariousInputs) {
    auto input = GetParam();
    Status result = processor_.ProcessData(input);
    EXPECT_NE(result, Status::kTimeout);
}

INSTANTIATE_TEST_SUITE_P(
    VariousInputs,
    DataProcessorParameterizedTest,
    ::testing::Values(
        std::vector<std::string>{"single"},
        std::vector<std::string>{"multiple", "items"},
        std::vector<std::string>{"many", "different", "values", "here"}
    )
);

// Mock example
class MockDataProcessor : public IDataProcessor {
public:
    MOCK_METHOD(Status, ProcessData, (const std::vector<std::string>& input), (override));
    MOCK_METHOD(std::optional<std::string>, GetResult, (), (const, override));
};

TEST(DataProcessorMockTest, ClientUsesProcessorCorrectly) {
    // Arrange
    MockDataProcessor mock_processor;
    std::vector<std::string> test_input{"test"};
    
    EXPECT_CALL(mock_processor, ProcessData(test_input))
        .WillOnce(::testing::Return(Status::kSuccess));
    
    // Act & Assert
    Client client(&mock_processor);
    bool result = client.ProcessWithProcessor(test_input);
    EXPECT_TRUE(result);
}

}  // namespace test
}  // namespace project_name
```

### Performance and Benchmark Tests
```cpp
#include <chrono>
#include <random>

namespace project_name {
namespace benchmark {

class PerformanceTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Generate test data
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(1, 1000);
        
        test_data_.reserve(10000);
        for (int i = 0; i < 10000; ++i) {
            test_data_.push_back("data_" + std::to_string(dis(gen)));
        }
    }
    
    std::vector<std::string> test_data_;
};

TEST_F(PerformanceTest, ProcessLargeDatasetWithinTimeLimit) {
    DataProcessor processor(test_data_.size());
    
    auto start = std::chrono::high_resolution_clock::now();
    Status result = processor.ProcessData(test_data_);
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    EXPECT_EQ(result, Status::kSuccess);
    EXPECT_LT(duration.count(), 1000);  // Should complete within 1 second
}

}  // namespace benchmark
}  // namespace project_name
```

## Configuration and Build Management

### CMake Best Practices
```cmake
# CMakeLists.txt for library
add_library(${PROJECT_NAME}_lib
    src/core/engine.cpp
    src/utils/string_utils.cpp
)

# Set properties
set_target_properties(${PROJECT_NAME}_lib PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    POSITION_INDEPENDENT_CODE ON
)

# Include directories
target_include_directories(${PROJECT_NAME}_lib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Link libraries
target_link_libraries(${PROJECT_NAME}_lib
    PUBLIC
        spdlog::spdlog
    PRIVATE
        ${CMAKE_THREAD_LIBS_INIT}
)

# Compiler-specific options
target_compile_options(${PROJECT_NAME}_lib PRIVATE
    $<$<CXX_COMPILER_ID:GNU>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
)
```

### Logging and Debugging
```cpp
#include <spdlog/spdlog.h>
#include <spdlog/sinks/file_sinks.h>
#include <spdlog/sinks/stdout_color_sinks.h>

namespace project_name {

class Logger {
public:
    static void Initialize() {
        // Create multi-sink logger
        auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
        auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>("logs/app.log", true);
        
        std::vector<spdlog::sink_ptr> sinks{console_sink, file_sink};
        auto logger = std::make_shared<spdlog::logger>("multi_sink", sinks.begin(), sinks.end());
        
        logger->set_level(spdlog::level::debug);
        logger->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%l] [%n] %v");
        
        spdlog::register_logger(logger);
        spdlog::set_default_logger(logger);
    }
    
    template<typename... Args>
    static void Info(const std::string& format, Args&&... args) {
        spdlog::info(format, std::forward<Args>(args)...);
    }
    
    template<typename... Args>
    static void Error(const std::string& format, Args&&... args) {
        spdlog::error(format, std::forward<Args>(args)...);
    }
};

// Usage example
void ExampleFunction() {
    Logger::Info("Processing started with {} items", 100);
    
    try {
        // Some processing...
        Logger::Info("Processing completed successfully");
    } catch (const std::exception& e) {
        Logger::Error("Processing failed: {}", e.what());
        throw;
    }
}

}  // namespace project_name
```

## Performance Optimization

### Efficient Data Structures and Algorithms
```cpp
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <execution>

namespace project_name {

class OptimizedProcessor {
private:
    std::vector<Data> data_;
    std::unordered_map<std::string, size_t> index_map_;
    
public:
    // Use move semantics for efficiency
    void AddData(Data&& data) {
        index_map_[data.GetKey()] = data_.size();
        data_.emplace_back(std::move(data));
    }
    
    // Range-based for loops
    void ProcessAll() {
        for (auto& data : data_) {
            data.Process();
        }
    }
    
    // STL algorithms with execution policies (C++17)
    void ParallelProcess() {
        std::for_each(std::execution::par_unseq,
                      data_.begin(), data_.end(),
                      [](Data& data) { data.Process(); });
    }
    
    // Efficient searching with hash map
    std::optional<Data*> FindByKey(const std::string& key) {
        auto it = index_map_.find(key);
        if (it != index_map_.end()) {
            return &data_[it->second];
        }
        return std::nullopt;
    }
    
    // Reserve memory to avoid reallocations
    void ReserveCapacity(size_t capacity) {
        data_.reserve(capacity);
        index_map_.reserve(capacity);
    }
};

}  // namespace project_name
```

## Best Practices Summary

1. **Use modern C++** - leverage C++17/C++20 features for cleaner, safer code
2. **Follow RAII principle** - automatic resource management through constructors/destructors
3. **Prefer smart pointers** - avoid manual memory management and raw pointers
4. **Write const-correct code** - use const wherever possible for better optimization
5. **Use move semantics** - implement move constructors and assignment operators
6. **Handle exceptions properly** - use RAII and exception-safe code patterns
7. **Write comprehensive tests** - unit tests, integration tests, and performance tests
8. **Use static analysis tools** - clang-tidy, cppcheck, and sanitizers
9. **Document interfaces clearly** - use comments for public APIs and complex algorithms
10. **Optimize judiciously** - profile first, then optimize hotspots with modern C++ techniques