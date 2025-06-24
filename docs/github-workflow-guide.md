# GitHub Workflow Guide for SwarmRouter Development

## Overview

This guide demonstrates professional GitHub workflows for contributing to the SwarmRouter project. Following these practices ensures code quality, enables collaboration, and provides clear documentation of changes.

## Workflow Steps

### 1. Create an Issue First

Before starting work, create or claim an issue:

```markdown
**Issue Title**: [HIVE-4.1] Implement HIVE Visualizer Module

**Description**:
Add a Ring 4 visualization module to the HIVE system that provides real-time monitoring of system activity through a Streamlit dashboard.

**Acceptance Criteria**:
- [ ] Ring topology visualization
- [ ] Active swarm monitoring  
- [ ] Performance metrics display
- [ ] Llama-bee metadata integration
- [ ] Docker configuration

**Labels**: `enhancement`, `ring-4`, `visualization`
**Assignee**: @your-username
```

### 2. Create a Feature Branch

```bash
# Ensure you're on main and up to date
git checkout main
git pull origin main

# Create feature branch following naming convention
git checkout -b feature/hive-visualizer-module

# Alternative naming patterns:
# bugfix/issue-description
# docs/what-you-are-documenting
# refactor/what-you-are-refactoring
```

### 3. Make Your Changes

Follow the commit message conventions:

```bash
# Stage specific files (not everything)
git add docs/hive-visualizer-module.md
git add docs/llama-bee-metadata.md

# Write descriptive commit messages
git commit -m "feat(visualizer): Add HIVE visualizer module specification

- Define Ring 4 module structure
- Create Streamlit dashboard design
- Add llama-bee metadata system
- Include Docker configuration

Relates to #4"

# More commits as you work
git add src/hive_visualizer/module.py
git commit -m "feat(visualizer): Implement core visualizer module

- Add HiveVisualizerModule class
- Implement ring topology rendering
- Add performance metrics collection
- Create event subscription handlers"
```

### 4. Keep Your Branch Updated

```bash
# Periodically sync with main
git checkout main
git pull origin main
git checkout feature/hive-visualizer-module
git rebase main

# If conflicts occur, resolve them
git status
# Edit conflicted files
git add <resolved-files>
git rebase --continue
```

### 5. Push Your Branch

```bash
# First push
git push -u origin feature/hive-visualizer-module

# Subsequent pushes
git push

# If you rebased, you may need to force push
git push --force-with-lease
```

### 6. Create a Pull Request

Use the GitHub UI or CLI:

```bash
# Using GitHub CLI
gh pr create --title "feat: Add HIVE Visualizer Module (Ring 4)" \
  --body "$(cat <<'EOF'
## Summary
This PR implements the HIVE Visualizer module as a Ring 4 component, providing real-time visualization of system activity through a Streamlit dashboard.

## Changes
- Added ring-based architecture documentation
- Implemented visualizer module with Streamlit integration
- Created llama-bee metadata system for visual representation
- Added Docker configuration for easy deployment

## Screenshots
[Add screenshots of the visualizer here]

## Testing
- [ ] Module loads successfully in Ring 4
- [ ] Streamlit dashboard renders correctly
- [ ] Real-time updates work as expected
- [ ] Performance metrics are accurate

## Related Issues
Closes #4

## Checklist
- [x] Code follows project style guidelines
- [x] Tests have been added/updated
- [x] Documentation has been updated
- [x] Changes have been tested locally
- [ ] PR has been reviewed by at least one team member
EOF
)"
```

### 7. Respond to Code Review

Example responses to common review feedback:

```markdown
# Acknowledging feedback
> "This function seems complex, could we break it down?"

Good point! I'll refactor this into smaller functions for better readability.

# Explaining decisions
> "Why did you choose Streamlit over Dash?"

Streamlit was chosen because:
1. Faster development cycle for MVPs
2. Better integration with our Python stack
3. Lower learning curve for contributors

# Making requested changes
> "Please add error handling here"

Added try-except block with appropriate error logging in commit 7f3a9c2
```

### 8. Update Based on Feedback

```bash
# Make requested changes
git add -p  # Interactively stage changes
git commit -m "refactor(visualizer): Address PR feedback

- Break down complex render function
- Add error handling for event subscriptions
- Improve performance metric calculations
- Add unit tests for core functionality"

git push
```

### 9. Merge the PR

Once approved:

```bash
# If using GitHub UI, select "Squash and merge" to keep history clean

# If merging locally (maintainers only)
git checkout main
git pull origin main
git merge --squash feature/hive-visualizer-module
git commit -m "feat: Add HIVE Visualizer Module (Ring 4) (#PR-number)

[Combined commit message summarizing all changes]

Co-authored-by: ReviewerName <reviewer@email.com>"
git push origin main
```

### 10. Clean Up

```bash
# Delete local branch
git branch -d feature/hive-visualizer-module

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/hive-visualizer-module
```

## Best Practices for Students

### Commit Message Format

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or updates
- `chore`: Build process or auxiliary tool changes

### PR Size Guidelines

Keep PRs focused and reviewable:
- **Ideal**: 200-400 lines of code
- **Maximum**: 1000 lines (break into multiple PRs if larger)
- **Files**: Preferably under 10 files per PR

### Documentation Requirements

Every PR should include:
1. **What**: Clear description of changes
2. **Why**: Motivation and context
3. **How**: Technical approach if non-obvious
4. **Testing**: How to verify the changes

### Code Review Etiquette

As a reviewer:
```markdown
# Good feedback
"Consider using a dictionary here for O(1) lookups instead of a list"

# Not helpful
"This is wrong"

# Suggesting improvements
"What do you think about extracting this into a separate method for reusability?"

# Acknowledging good work
"Nice use of the strategy pattern here! 👍"
```

As a reviewee:
- Respond to all comments
- Ask for clarification if needed
- Thank reviewers for their time
- Update PR description with changes made

## Example Student Workflow

```bash
# Monday: Start new feature
git checkout -b feature/add-bee-metrics
# Work on feature...

# Tuesday: Continue work
git add -A
git commit -m "WIP: bee metrics"  # OK for local work

# Wednesday: Clean up before PR
git rebase -i HEAD~3  # Squash WIP commits
# Rewrite commit messages properly

# Thursday: Create PR
git push -u origin feature/add-bee-metrics
gh pr create

# Friday: Address review feedback
git add -u
git commit -m "address review feedback"
git push
```

## Common Mistakes to Avoid

1. **Committing to main**: Always use feature branches
2. **Large PRs**: Break down into smaller, focused changes
3. **Poor commit messages**: "fix stuff" helps no one
4. **Not testing locally**: Always test before pushing
5. **Ignoring CI failures**: Fix tests before requesting review
6. **Not updating docs**: Code without docs is incomplete

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [The Art of Code Review](https://google.github.io/eng-practices/review/)

Remember: Good Git practices are a professional skill that will serve you throughout your career!