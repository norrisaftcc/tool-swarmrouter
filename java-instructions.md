# Java Coding Instructions

## Project Overview

This document provides comprehensive coding standards and best practices for Java development. These guidelines ensure code consistency, maintainability, and adherence to Java enterprise standards across all Java-based projects.

## Code Formatting Standards

### Required Tools
- **Checkstyle**: Code style and standards enforcement
- **SpotBugs**: Static analysis for bug detection
- **PMD**: Source code analyzer for common programming flaws
- **Google Java Format** or **Eclipse Formatter**: Code formatting

### Configuration
Set up your development environment with these tools:
```bash
# Using Maven plugins
mvn checkstyle:check
mvn spotbugs:check
mvn pmd:check

# Using Gradle plugins
./gradlew checkstyleMain
./gradlew spotbugsMain
./gradlew pmdMain
```

### IDE Configuration
Configure your IDE to:
- Use consistent code formatting (Google Java Style or similar)
- Show Checkstyle violations inline
- Enable auto-formatting on save
- Use 4 spaces for indentation (or 2 spaces if following Google Style)
- Set line length to 100 characters

## Development Workflow

### Environment Setup
1. Use Java 11+ (LTS versions recommended: 11, 17, 21)
2. Set up build tool (Maven 3.6+ or Gradle 7+)
3. Configure IDE with project-specific settings
4. Install required development plugins

### Build Tool Setup

#### Maven Configuration
```xml
<!-- pom.xml -->
<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <junit.version>5.9.0</junit.version>
    <spring.boot.version>3.0.0</spring.boot.version>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.2.0</version>
            <configuration>
                <configLocation>checkstyle.xml</configLocation>
            </configuration>
        </plugin>
    </plugins>
</build>
```

#### Gradle Configuration
```gradle
// build.gradle
plugins {
    id 'java'
    id 'checkstyle'
    id 'pmd'
    id 'com.github.spotbugs' version '5.0.13'
}

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

checkstyle {
    toolVersion = '10.3.4'
    configFile = file('checkstyle.xml')
}
```

### Development Commands
```bash
# Build project
mvn clean compile
# or
./gradlew build

# Run tests
mvn test
# or
./gradlew test

# Generate test coverage
mvn jacoco:report
# or
./gradlew jacocoTestReport

# Static analysis
mvn checkstyle:check spotbugs:check pmd:check
# or
./gradlew check

# Package application
mvn package
# or
./gradlew bootJar
```

## Repository Structure

```
project-name/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/company/project/
│   │   │       ├── ProjectApplication.java    # Main application class
│   │   │       ├── controller/               # REST controllers
│   │   │       ├── service/                  # Business logic services
│   │   │       ├── repository/               # Data access layer
│   │   │       ├── model/                    # Entity and DTO classes
│   │   │       ├── config/                   # Configuration classes
│   │   │       └── util/                     # Utility classes
│   │   └── resources/
│   │       ├── application.yml               # Application configuration
│   │       ├── static/                       # Static web resources
│   │       └── templates/                    # Template files
│   └── test/
│       ├── java/
│       │   └── com/company/project/
│       │       ├── unit/                     # Unit tests
│       │       ├── integration/              # Integration tests
│       │       └── TestApplication.java     # Test configuration
│       └── resources/
│           └── application-test.yml          # Test configuration
├── docs/                                     # Documentation
├── scripts/                                  # Build and deployment scripts
├── pom.xml                                   # Maven configuration
├── build.gradle                              # Gradle configuration (alternative)
├── checkstyle.xml                            # Checkstyle rules
├── .gitignore                                # Git ignore patterns
└── README.md                                 # Project documentation
```

## Development Guidelines

### Java Code Style
- Follow **Java naming conventions** strictly
- Use `camelCase` for variables and methods
- Use `PascalCase` for class names
- Use `UPPER_SNAKE_CASE` for constants
- Write self-documenting code with clear names
- Keep methods focused and under 30 lines

### Object-Oriented Design Principles
```java
// Use interfaces and dependency injection
public interface UserService {
    User findById(Long id);
    User save(User user);
    void deleteById(Long id);
}

@Service
@Transactional
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    
    // Constructor injection (preferred)
    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    @Override
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
    }
}
```

### Exception Handling
```java
// Custom exceptions
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
    
    public UserNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}

// Global exception handler (Spring Boot)
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("USER_NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
}
```

### Data Models and Validation
```java
// Entity class
@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    @Size(min = 1, max = 100)
    private String name;
    
    @Column(unique = true, nullable = false)
    @Email
    private String email;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Constructors, getters, setters
    public User() {}
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }
    
    // Standard getters and setters
    // equals(), hashCode(), toString() methods
}

// DTO class
public class UserDto {
    
    @NotBlank(message = "Name is required")
    @Size(max = 100, message = "Name must be less than 100 characters")
    private String name;
    
    @NotBlank(message = "Email is required")
    @Email(message = "Email must be valid")
    private String email;
    
    // Constructors, getters, setters
}
```

## Testing Strategy

### Testing Framework
- Use **JUnit 5** as the primary testing framework
- Use **Mockito** for mocking dependencies
- Use **TestContainers** for integration testing with real databases
- Use **Spring Boot Test** for Spring-based applications

### Test Categories
```java
// Unit tests
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserServiceImpl userService;
    
    @Test
    @DisplayName("Should find user by ID successfully")
    void shouldFindUserByIdSuccessfully() {
        // Given
        Long userId = 1L;
        User expectedUser = new User("John Doe", "john@example.com");
        when(userRepository.findById(userId)).thenReturn(Optional.of(expectedUser));
        
        // When
        User actualUser = userService.findById(userId);
        
        // Then
        assertThat(actualUser).isEqualTo(expectedUser);
        verify(userRepository).findById(userId);
    }
    
    @Test
    @DisplayName("Should throw exception when user not found")
    void shouldThrowExceptionWhenUserNotFound() {
        // Given
        Long userId = 1L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());
        
        // When & Then
        assertThatThrownBy(() -> userService.findById(userId))
            .isInstanceOf(UserNotFoundException.class)
            .hasMessage("User not found: " + userId);
    }
}

// Integration tests
@SpringBootTest
@Testcontainers
@Transactional
class UserServiceIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @Autowired
    private UserService userService;
    
    @Test
    @DisplayName("Should save and retrieve user from database")
    void shouldSaveAndRetrieveUser() {
        // Given
        User user = new User("Jane Doe", "jane@example.com");
        
        // When
        User savedUser = userService.save(user);
        User retrievedUser = userService.findById(savedUser.getId());
        
        // Then
        assertThat(retrievedUser.getName()).isEqualTo("Jane Doe");
        assertThat(retrievedUser.getEmail()).isEqualTo("jane@example.com");
    }
}
```

### Test Coverage
- Maintain >80% test coverage for service layer
- Focus on testing business logic and edge cases
- Use integration tests for database operations
- Mock external dependencies in unit tests

## Configuration Management

### Application Configuration
```yaml
# application.yml
spring:
  application:
    name: my-application
  
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:development}
  
  datasource:
    url: ${DATABASE_URL:jdbc:h2:mem:testdb}
    username: ${DATABASE_USERNAME:sa}
    password: ${DATABASE_PASSWORD:}
    driver-class-name: ${DATABASE_DRIVER:org.h2.Driver}
  
  jpa:
    hibernate:
      ddl-auto: ${JPA_DDL_AUTO:validate}
    show-sql: ${JPA_SHOW_SQL:false}
    properties:
      hibernate:
        dialect: ${JPA_DIALECT:org.hibernate.dialect.H2Dialect}

logging:
  level:
    com.company.project: ${LOG_LEVEL:INFO}
    org.springframework.security: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"

# Custom application properties
app:
  api:
    base-url: ${API_BASE_URL:http://localhost:8080}
    timeout: ${API_TIMEOUT:30000}
  security:
    jwt:
      secret: ${JWT_SECRET:your-secret-key}
      expiration: ${JWT_EXPIRATION:86400000}
```

### Configuration Classes
```java
@Configuration
@ConfigurationProperties(prefix = "app")
@Data
public class ApplicationProperties {
    
    private Api api = new Api();
    private Security security = new Security();
    
    @Data
    public static class Api {
        private String baseUrl;
        private int timeout;
    }
    
    @Data
    public static class Security {
        private Jwt jwt = new Jwt();
        
        @Data
        public static class Jwt {
            private String secret;
            private long expiration;
        }
    }
}
```

## Logging

### Structured Logging
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

@Service
public class UserService {
    
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    
    public User processUser(Long userId) {
        // Add correlation ID for request tracing
        MDC.put("userId", userId.toString());
        MDC.put("operation", "processUser");
        
        try {
            logger.info("Starting user processing");
            
            User user = findById(userId);
            logger.info("User found: {}", user.getName());
            
            // Process user...
            
            logger.info("User processing completed successfully");
            return user;
            
        } catch (Exception e) {
            logger.error("Error processing user: {}", e.getMessage(), e);
            throw e;
        } finally {
            MDC.clear();
        }
    }
}
```

## Security Best Practices

### Input Validation
```java
@RestController
@RequestMapping("/api/users")
@Validated
public class UserController {
    
    @PostMapping
    public ResponseEntity<UserDto> createUser(@Valid @RequestBody UserDto userDto) {
        // Input is automatically validated by @Valid annotation
        User user = userService.createUser(userDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(mapToDto(user));
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable @Min(1) Long id) {
        User user = userService.findById(id);
        return ResponseEntity.ok(mapToDto(user));
    }
}
```

### Database Security
```java
// Use parameterized queries to prevent SQL injection
@Repository
public class UserRepositoryImpl {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    public List<User> findByNameContaining(String namePattern) {
        String sql = "SELECT u FROM User u WHERE u.name LIKE :pattern";
        return entityManager.createQuery(sql, User.class)
            .setParameter("pattern", "%" + namePattern + "%")
            .getResultList();
    }
}
```

## Build and Deployment

### Maven Build Configuration
```xml
<profiles>
    <profile>
        <id>development</id>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
        <properties>
            <spring.profiles.active>development</spring.profiles.active>
        </properties>
    </profile>
    
    <profile>
        <id>production</id>
        <properties>
            <spring.profiles.active>production</spring.profiles.active>
        </properties>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                    <configuration>
                        <layers>
                            <enabled>true</enabled>
                        </layers>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM openjdk:11-jre-slim

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Best Practices Summary

1. **Follow Java conventions** - consistent naming and code organization
2. **Use dependency injection** - prefer constructor injection over field injection
3. **Write comprehensive tests** - unit tests for logic, integration tests for full workflows
4. **Handle exceptions properly** - specific exceptions with meaningful messages
5. **Validate input data** - use Bean Validation annotations
6. **Implement proper logging** - structured logging with correlation IDs
7. **Use configuration profiles** - separate settings for different environments
8. **Follow security practices** - input validation, parameterized queries, secure configurations
9. **Maintain code quality** - use static analysis tools and code reviews
10. **Document APIs** - use OpenAPI/Swagger for REST API documentation