# Beta Multi-Agent Workflow Guide

## Overview

This is a simplified, junior-friendly version of the comprehensive multi-agent workflow, designed to be easier to follow while retaining core best practices. Perfect for developers new to AI-assisted development or teams getting started with LLM tools.

## Getting Started (5 Minutes)

### What You'll Need
- **GitHub account** with access to the repository
- **AI assistant** (GitHub Copilot, Claude, or similar)
- **Python development environment** (VS Code recommended)
- **Basic Git knowledge** (clone, commit, push, pull)

### First-Time Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/norrisaftcc/tool-swarmrouter.git
   cd tool-swarmrouter
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your AI assistant**
   - Install GitHub Copilot extension in VS Code, OR
   - Set up Claude Dev extension, OR
   - Configure your preferred AI coding assistant

## Simple Workflow (Just 4 Steps!)

### Step 1: Pick Your Task
Start with issues labeled `good first issue` or `beginner-friendly`:

```markdown
**Look for these labels:**
- 🟢 `good first issue` - Perfect for beginners
- 🟡 `help wanted` - Team needs assistance
- 🔵 `documentation` - Usually straightforward
- 🟠 `ai-assisted` - AI tools will help you
```

### Step 2: Create Your Branch
Keep it simple with a clear naming pattern:

```bash
# Always start from main
git checkout main
git pull origin main

# Create your branch (use your name + brief description)
git checkout -b yourname/issue-123-add-feature
```

**Branch naming examples:**
- `sarah/issue-45-fix-login`
- `mike/issue-67-update-docs`
- `alex/issue-89-add-tests`

### Step 3: Code with AI Help
Use your AI assistant throughout the development process:

#### 🤖 Ask AI for Help
```bash
# In your IDE or chat:
"@copilot help me implement a function that..."
"@claude review this code for bugs"
"Can you help me write tests for this function?"
```

#### ✅ Basic Code Quality Checks
Before committing, run these simple commands:
```bash
# Format your code
black .

# Check for obvious issues
flake8 . --count --select=E9,F63,F7,F82 --show-source

# Run basic tests
pytest
```

#### 📝 Write Simple Commit Messages
```bash
git add .
git commit -m "fix: resolve login timeout issue

- Added timeout handling in auth.py
- Updated error messages for clarity
- Added basic test coverage

Fixes #123"
```

### Step 4: Submit and Collaborate
Create a pull request and get feedback:

#### 📤 Push Your Changes
```bash
git push -u origin yourname/issue-123-add-feature
```

#### 🔄 Create Pull Request
Use GitHub's web interface and include:

```markdown
## What I Changed
- Fixed the login timeout issue
- Added better error handling
- Wrote tests to prevent regression

## How to Test
1. Run the application
2. Try logging in with slow internet
3. Verify error message is clear

## AI Tools Used
- GitHub Copilot for code suggestions
- AI-generated test cases
- Automated code formatting

## Checklist
- [x] Code works locally
- [x] Added/updated tests
- [x] Code is formatted (black)
- [x] AI review completed
- [ ] Team review pending
```

## AI Assistant Quick Guide

### 🚀 Quick AI Commands

#### Code Generation
```bash
# Ask AI to generate code
"Write a Python function that validates email addresses"
"Create a FastAPI endpoint for user registration"
"Generate unit tests for this function"
```

#### Code Review
```bash
# Ask AI to review your code
"Review this code for bugs and improvements"
"Check this function for security issues"
"Suggest better variable names"
```

#### Documentation
```bash
# Ask AI to help with docs
"Write a docstring for this function"
"Explain what this code does"
"Create a README section for this feature"
```

### 🎯 AI Best Practices (Keep It Simple)

#### Do's ✅
- **Ask specific questions**: "How do I handle this error?" vs "Help me"
- **Review AI suggestions**: Don't blindly accept everything
- **Test AI-generated code**: Always run tests after AI changes
- **Keep learning**: Ask AI to explain concepts you don't understand

#### Don'ts ❌
- **Don't copy-paste without understanding**: Ask AI to explain first
- **Don't skip testing**: AI makes mistakes too
- **Don't ignore warnings**: Address linting and type errors
- **Don't work alone**: Ask teammates when stuck

## Simple Quality Checklist

Before submitting your pull request, check these boxes:

### Code Quality ✅
- [ ] **Code runs without errors** (test it locally)
- [ ] **AI reviewed the code** (ask your AI assistant to check it)
- [ ] **Code is formatted** (run `black .`)
- [ ] **No obvious bugs** (run basic linting)

### Testing ✅
- [ ] **Basic tests pass** (run `pytest`)
- [ ] **New code has tests** (AI can help write them)
- [ ] **Manual testing done** (try the feature yourself)

### Documentation ✅
- [ ] **Code has comments** (explain complex parts)
- [ ] **Function docstrings added** (AI can generate these)
- [ ] **README updated if needed** (for new features)

### Collaboration ✅
- [ ] **Clear commit messages** (explain what and why)
- [ ] **Pull request description** (what changed, how to test)
- [ ] **Linked to issue** (include "Fixes #123")

## Common Tasks with AI Help

### 🐛 Fixing Bugs

1. **Understand the bug**
   ```bash
   # Ask AI to help analyze
   "@copilot explain this error message"
   "What could cause this bug?"
   ```

2. **Find the problem**
   ```bash
   # Use AI to review code
   "@copilot review this function for potential bugs"
   "Check this code for edge cases"
   ```

3. **Fix and test**
   ```bash
   # Ask AI for fix suggestions
   "@copilot suggest a fix for this bug"
   "Write a test that reproduces this bug"
   ```

### ✨ Adding Features

1. **Plan with AI**
   ```bash
   # Ask for implementation approach
   "@copilot how should I implement this feature?"
   "What's the best way to structure this code?"
   ```

2. **Implement step by step**
   ```bash
   # Break it down
   "Help me implement just the core logic first"
   "Now add error handling"
   "Finally add the tests"
   ```

3. **Review and improve**
   ```bash
   # Ask for improvements
   "@copilot how can I make this code better?"
   "Are there any security concerns?"
   ```

### 📚 Writing Tests

1. **Ask AI for test ideas**
   ```bash
   "@copilot write unit tests for this function"
   "What edge cases should I test?"
   "Generate integration tests for this API"
   ```

2. **Use AI-generated test templates**
   ```python
   # AI can help create test structure
   def test_user_login():
       # Arrange - AI helps set up test data
       # Act - AI helps call the function
       # Assert - AI helps verify results
   ```

## Simplified CI/CD

Your code goes through these automatic checks (don't worry, AI helps fix issues):

### 🔄 Automatic Checks
1. **Code Formatting**: Ensures consistent style
2. **Basic Linting**: Catches obvious errors
3. **Test Execution**: Runs your tests
4. **AI Code Review**: Automated quality check

### 🚨 If Checks Fail
1. **Read the error message** (GitHub shows what failed)
2. **Ask AI for help**: "@copilot help me fix this CI error"
3. **Make changes locally** and push again
4. **Ask teammates** if you're stuck

## Getting Help

### 🤝 When to Ask for Human Help
- **Complex architectural decisions**: "Should I use a database here?"
- **Domain-specific knowledge**: "How does our authentication work?"
- **Stuck for more than 2 hours**: Don't struggle alone!
- **Security concerns**: Always double-check with the team

### 🤖 When to Ask AI
- **Code syntax questions**: "How do I write this in Python?"
- **Error debugging**: "What does this error mean?"
- **Test writing**: "Help me test this function"
- **Code improvement**: "Make this code more readable"

### 📚 Learning Resources
- **AI-Generated Examples**: Ask AI to show examples of patterns
- **Code Comments**: Ask AI to explain complex code
- **Documentation**: Use AI to understand documentation
- **Practice**: Ask AI for coding exercises

## Quick Reference

### 📋 Daily Workflow Checklist
1. [ ] **Start day**: Pull latest changes (`git pull origin main`)
2. [ ] **Pick task**: Choose from `good first issue` labels
3. [ ] **Create branch**: Use clear naming (`yourname/issue-123-description`)
4. [ ] **Code with AI**: Use AI assistant throughout development
5. [ ] **Test locally**: Run tests and manual testing
6. [ ] **Format code**: Run `black .` before committing
7. [ ] **Commit changes**: Write clear commit messages
8. [ ] **Create PR**: Include clear description and checklist
9. [ ] **Address feedback**: Respond to review comments
10. [ ] **Celebrate**: You're contributing to the project! 🎉

### 🛠️ Essential Commands
```bash
# Daily commands you'll use
git pull origin main              # Get latest changes
git checkout -b your-branch       # Create new branch
black .                          # Format code
pytest                           # Run tests
git add . && git commit -m "msg"  # Save changes
git push -u origin your-branch   # Upload changes
```

### 🤖 AI Helper Phrases
```bash
# Copy-paste these into your AI assistant
"@copilot explain this error"
"@copilot review this code"
"@copilot write tests for this"
"@copilot make this more readable"
"@copilot check for bugs"
"@copilot suggest improvements"
```

## Success Tips for Beginners

### 🎯 Start Small
- **Choose simple issues first**: Build confidence gradually
- **One change at a time**: Don't try to fix everything at once
- **Ask questions early**: Better to ask than struggle alone

### 🤝 Collaborate Effectively
- **Communicate progress**: Update issues with your progress
- **Share what you learn**: Help other beginners too
- **Be patient**: Learning takes time, but AI makes it faster

### 🔄 Iterate and Improve
- **Learn from feedback**: Each review teaches you something
- **Practice regularly**: Consistency beats intensity
- **Celebrate small wins**: Every contribution matters

---

## What's Next?

Once you're comfortable with this beta workflow, consider exploring:

- **Advanced AI Tools**: More sophisticated AI assistants and features
- **Full Workflow**: Graduate to the comprehensive multi-agent workflow
- **Mentoring Others**: Help new developers get started
- **Tool Customization**: Configure AI tools for your specific needs

Remember: **This workflow grows with you!** Start simple, use AI to learn faster, and gradually take on more complex challenges. The AI is your coding buddy - use it to learn, not as a replacement for understanding.

---

*Need help? Ask in the team chat or create an issue with the `help wanted` label. Someone (human or AI) will help you! 🚀*