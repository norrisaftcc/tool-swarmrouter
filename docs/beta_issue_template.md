# Beta Issue Template - Simplified for Beginners

## Basic Information

**Title**: [COMPONENT] Brief description of what needs to be done
**Type**: Bug Fix | New Feature | Documentation | Test | Improvement
**Priority**: High | Medium | Low
**Difficulty**: Beginner | Intermediate | Advanced
**Time Estimate**: 1-2 hours | Half day | Full day | 2-3 days

## What Needs to Be Done?

### Simple Description
*Explain what you want to accomplish in plain language*

Example: "Add a button that lets users save their preferences"

### Why Is This Important?
*Explain why this matters to users or the project*

Example: "Users currently lose their settings when they refresh the page"

### Who Will Use This?
*Describe who benefits from this change*

Example: "All users who want to customize their experience"

## Requirements (Checklist)

### Must Have ✅
- [ ] **Main functionality works**: Core feature/fix is implemented
- [ ] **No errors**: Code runs without crashing
- [ ] **Basic testing**: Manually tested the changes
- [ ] **Code is clean**: Formatted and readable

### Should Have 📋
- [ ] **Has tests**: Automated tests for the new code
- [ ] **Documentation**: Comments explaining complex parts
- [ ] **Error handling**: Graceful handling of problems
- [ ] **User-friendly**: Good experience for end users

### Nice to Have 🌟
- [ ] **Performance optimized**: Runs efficiently
- [ ] **Accessible**: Works for users with disabilities
- [ ] **Mobile-friendly**: Works on phones/tablets
- [ ] **Well-documented**: Full documentation updates

## AI Assistance Plan

### How Will AI Help? 🤖
- [ ] **Planning**: Ask AI to suggest implementation approach
- [ ] **Coding**: Use AI for code generation and suggestions
- [ ] **Testing**: Get AI help writing tests
- [ ] **Review**: Use AI to check code quality
- [ ] **Documentation**: AI assistance with comments and docs

### AI Tools to Use
- [ ] **GitHub Copilot**: Code suggestions while typing
- [ ] **Claude/ChatGPT**: Planning and problem-solving
- [ ] **AI Code Review**: Automated quality checks
- [ ] **AI Documentation**: Help with comments and docs

## Step-by-Step Plan

### Step 1: Understand the Problem
- [ ] **Read the issue carefully**: Make sure you understand what's needed
- [ ] **Ask questions**: If anything is unclear, ask for clarification
- [ ] **Research similar code**: Look at how similar features are implemented
- [ ] **Ask AI for guidance**: "@ai explain how I should approach this"

### Step 2: Plan Your Approach
- [ ] **Break it down**: What files will you need to change?
- [ ] **Identify dependencies**: What other parts of the code will this affect?
- [ ] **Plan your tests**: How will you verify it works?
- [ ] **Ask AI for suggestions**: "@ai what's the best way to implement this?"

### Step 3: Implement and Test
- [ ] **Start small**: Get basic functionality working first
- [ ] **Test frequently**: Check your changes work as you go
- [ ] **Use AI help**: Get suggestions for improvements
- [ ] **Add error handling**: Make sure edge cases are covered

### Step 4: Review and Polish
- [ ] **Self-review**: Read through your changes
- [ ] **AI review**: Ask AI to check for issues
- [ ] **Format code**: Run code formatting tools
- [ ] **Update documentation**: Add comments and update docs

## Technical Details (Fill in what you know)

### Files That Might Need Changes
- **Main file**: `src/[component]/[file].py` (if you know it)
- **Test file**: `tests/test_[component].py` (create if needed)
- **Documentation**: `docs/[relevant-doc].md` (if applicable)
- **Configuration**: Any config files that need updates

### Key Functions/Classes Involved
- **Function to modify**: `function_name()` (if you know it)
- **New function to create**: Describe what it should do
- **Classes involved**: List relevant classes
- **APIs/endpoints**: Any web endpoints affected

### External Dependencies
- **New libraries needed**: List any new dependencies
- **API calls**: External services this might use
- **Database changes**: Any data structure changes
- **Environment variables**: New configuration needed

## Testing Plan (Keep It Simple)

### Manual Testing Checklist
- [ ] **Happy path**: Test the main functionality works
- [ ] **Error cases**: Test what happens when things go wrong
- [ ] **Edge cases**: Test unusual but possible scenarios
- [ ] **User experience**: Make sure it's easy to use

### Automated Testing
- [ ] **Unit tests**: Test individual functions work correctly
- [ ] **Integration tests**: Test components work together
- [ ] **AI-generated tests**: Ask AI to suggest test cases
- [ ] **Existing tests pass**: Make sure you didn't break anything

### Test Examples
```python
# Example test structure (AI can help fill this in)
def test_new_feature():
    # Arrange - set up test data
    # Act - call the function being tested
    # Assert - check the result is correct
    pass
```

## Getting Help

### When to Ask for Human Help 🤝
- **Stuck for more than 1 hour**: Don't struggle alone!
- **Security concerns**: Always double-check security implications
- **Architecture decisions**: "Should I create a new file or modify existing?"
- **Complex business logic**: Domain-specific knowledge questions

### When to Ask AI 🤖
- **Syntax questions**: "How do I write this in Python?"
- **Error messages**: "What does this error mean?"
- **Code examples**: "Show me how to implement this pattern"
- **Testing ideas**: "What should I test for this function?"
- **Code review**: "Check this code for problems"

### Resources for Learning
- **Ask AI for explanations**: "Explain how this code works"
- **Code examples**: Request examples of similar features
- **Best practices**: "What are best practices for this type of code?"
- **Debugging help**: "Help me figure out why this isn't working"

## Definition of Done (Simplified)

### Code Complete ✅
- [ ] **Feature works**: Main functionality is implemented
- [ ] **No crashes**: Code runs without errors
- [ ] **Follows style**: Code is formatted consistently
- [ ] **Has comments**: Complex parts are explained

### Quality Checked ✅
- [ ] **AI reviewed**: Used AI tools to check code quality
- [ ] **Manually tested**: Tried the feature yourself
- [ ] **Tests added**: At least basic tests are included
- [ ] **No obvious bugs**: Code behaves as expected

### Ready to Share ✅
- [ ] **Clean commits**: Commit messages explain what changed
- [ ] **Documentation updated**: README or comments updated if needed
- [ ] **Issue linked**: Pull request references this issue
- [ ] **Ready for review**: Code is ready for team feedback

## Success Checklist

### Before You Start ✅
- [ ] **Understand the goal**: Clear on what needs to be accomplished
- [ ] **Have the right tools**: Development environment set up
- [ ] **Know how to get help**: Identified who/what to ask when stuck
- [ ] **Planned your approach**: Have a rough idea of what to do

### While Working ✅
- [ ] **Making progress**: Regular small commits showing progress
- [ ] **Testing as you go**: Checking changes work frequently
- [ ] **Using AI effectively**: Getting help from AI tools
- [ ] **Asking questions**: Reaching out when stuck

### When Finished ✅
- [ ] **Feature complete**: All requirements met
- [ ] **Quality assured**: Code reviewed and tested
- [ ] **Documentation current**: Relevant docs updated
- [ ] **Team ready**: Ready for code review and feedback

## Common Pitfalls to Avoid

### Beginner Mistakes ⚠️
- **Changing too much at once**: Keep changes small and focused
- **Not testing locally**: Always test before pushing code
- **Ignoring errors**: Address warnings and errors promptly
- **Working in isolation**: Communicate progress and blockers

### AI-Related Pitfalls ⚠️
- **Blindly accepting AI suggestions**: Always review and understand code
- **Not testing AI-generated code**: AI makes mistakes too
- **Over-relying on AI**: Balance AI help with your own learning
- **Not asking for clarification**: Ask AI to explain when confused

## Additional Notes

### Special Considerations
*Any special requirements, constraints, or considerations for this issue*

### Related Issues
- **Depends on**: #XXX (if this issue depends on another)
- **Blocks**: #YYY (if other issues depend on this)
- **Related to**: #ZZZ (if there are related issues)

### Team Context
- **Preferred approach**: If the team has a preferred implementation style
- **Existing patterns**: Reference similar implementations in the codebase
- **Architecture guidelines**: Any specific architectural requirements

---

## Issue Metadata

**Labels**: `beginner-friendly`, `ai-assisted`, `[component-name]`, `[priority-level]`
**Assignee**: @your-username
**Milestone**: [Sprint/Release name]
**Estimated Completion**: [Date]

**Created**: [Date]
**Last Updated**: [Date]

---

## Quick Start Template

*Copy this section when creating a new issue for quick setup:*

```markdown
## What: [One sentence description]
## Why: [One sentence business value]
## How: [Basic approach]
## AI Help: [Which AI tools will you use]
## Timeline: [Estimated time]
## Success: [How you'll know it's done]
```

---

*Remember: This is a learning opportunity! Use AI to help you succeed, ask questions when stuck, and celebrate your progress. Every expert was once a beginner! 🚀*