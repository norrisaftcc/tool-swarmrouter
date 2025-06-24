# GitHub Labels Setup for SwarmRouter

## Overview

This document defines the recommended GitHub labels for the SwarmRouter project. These labels help organize issues and PRs, making it easier for contributors to find work and understand the project status.

## Label Categories

### Type Labels (Blue - #0075ca)
- **enhancement** - New feature or request
- **bug** - Something isn't working
- **documentation** - Improvements or additions to documentation
- **refactor** - Code refactoring without changing functionality
- **test** - Adding or improving tests
- **chore** - Maintenance tasks (dependencies, build, etc.)

### Priority Labels (Red Shades)
- **critical** (#d73a4a) - Must be addressed immediately
- **high-priority** (#e4606d) - Important, address soon
- **medium-priority** (#f490a0) - Normal priority
- **low-priority** (#ffc0cb) - Nice to have, when time permits

### Component/Ring Labels (Purple - #7057ff)
- **ring-0** - Core system (MCP protocol, auth, database)
- **ring-1** - Essential dev tools (architect, orchestrator)
- **ring-2** - Extended tools (chronicler, intelligence)
- **ring-3** - External integrations (GitHub, Slack)
- **ring-4** - UI/Visualization (Observatory, dashboards)

### Tool-Specific Labels (Green - #0e8a16)
- **architect-tool** - Related to architect:* tools
- **orchestrator-tool** - Related to orchestrator:* tools
- **chronicler-tool** - Related to chronicler:* tools
- **intelligence-tool** - Related to intel:* tools

### Sprint/Milestone Labels (Orange - #d93f0b)
- **sprint-1** - Foundation sprint
- **sprint-2** - Core tools sprint
- **sprint-3** - Extended tools sprint
- **mvp** - Minimum viable product features
- **future** - Future enhancements

### Status Labels (Yellow - #fbca04)
- **in-progress** - Work has started
- **blocked** - Blocked by another issue or external factor
- **ready-for-review** - PR is ready for review
- **needs-discussion** - Requires team discussion
- **on-hold** - Temporarily paused

### Special Labels
- **good-first-issue** (#7057ff) - Good for newcomers
- **help-wanted** (#008672) - Extra attention is needed
- **student-friendly** (#0052cc) - Suitable for student contributors
- **learning-exercise** (#5319e7) - Designed for educational purposes
- **needs-tests** (#f9d0c4) - Tests need to be added
- **breaking-change** (#d73a4a) - Introduces breaking changes

## Setting Up Labels

### Using GitHub CLI

```bash
# Create all labels using gh CLI
# Note: Run these commands from the repository root

# Type labels
gh label create "enhancement" --description "New feature or request" --color "0075ca"
gh label create "bug" --description "Something isn't working" --color "0075ca"
gh label create "documentation" --description "Improvements or additions to documentation" --color "0075ca"
gh label create "refactor" --description "Code refactoring" --color "0075ca"
gh label create "test" --description "Adding or improving tests" --color "0075ca"
gh label create "chore" --description "Maintenance tasks" --color "0075ca"

# Priority labels
gh label create "critical" --description "Must be addressed immediately" --color "d73a4a"
gh label create "high-priority" --description "Important, address soon" --color "e4606d"
gh label create "medium-priority" --description "Normal priority" --color "f490a0"
gh label create "low-priority" --description "Nice to have" --color "ffc0cb"

# Ring labels
gh label create "ring-0" --description "Core system" --color "7057ff"
gh label create "ring-1" --description "Essential dev tools" --color "7057ff"
gh label create "ring-2" --description "Extended tools" --color "7057ff"
gh label create "ring-3" --description "External integrations" --color "7057ff"
gh label create "ring-4" --description "UI/Visualization" --color "7057ff"

# Tool labels
gh label create "architect-tool" --description "architect:* tools" --color "0e8a16"
gh label create "orchestrator-tool" --description "orchestrator:* tools" --color "0e8a16"
gh label create "chronicler-tool" --description "chronicler:* tools" --color "0e8a16"
gh label create "intelligence-tool" --description "intel:* tools" --color "0e8a16"

# Sprint labels
gh label create "sprint-1" --description "Foundation sprint" --color "d93f0b"
gh label create "sprint-2" --description "Core tools sprint" --color "d93f0b"
gh label create "sprint-3" --description "Extended tools sprint" --color "d93f0b"
gh label create "mvp" --description "Minimum viable product" --color "d93f0b"
gh label create "future" --description "Future enhancements" --color "d93f0b"

# Status labels
gh label create "in-progress" --description "Work has started" --color "fbca04"
gh label create "blocked" --description "Blocked by dependencies" --color "fbca04"
gh label create "ready-for-review" --description "PR ready for review" --color "fbca04"
gh label create "needs-discussion" --description "Requires team discussion" --color "fbca04"
gh label create "on-hold" --description "Temporarily paused" --color "fbca04"

# Special labels
gh label create "good-first-issue" --description "Good for newcomers" --color "7057ff"
gh label create "help-wanted" --description "Extra attention needed" --color "008672"
gh label create "student-friendly" --description "Suitable for students" --color "0052cc"
gh label create "learning-exercise" --description "Educational purpose" --color "5319e7"
gh label create "needs-tests" --description "Tests need to be added" --color "f9d0c4"
gh label create "breaking-change" --description "Breaking changes" --color "d73a4a"
```

### Bulk Setup Script

Create a script `setup-labels.sh`:

```bash
#!/bin/bash
# setup-labels.sh - Set up all GitHub labels for SwarmRouter

echo "Setting up GitHub labels for SwarmRouter..."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed. Please install it first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Not in a git repository. Please run from the repository root."
    exit 1
fi

# Create all labels
labels=(
    "enhancement:New feature or request:0075ca"
    "bug:Something isn't working:0075ca"
    "documentation:Documentation improvements:0075ca"
    "refactor:Code refactoring:0075ca"
    "test:Test improvements:0075ca"
    "chore:Maintenance tasks:0075ca"
    "critical:Must be addressed immediately:d73a4a"
    "high-priority:Important, address soon:e4606d"
    "medium-priority:Normal priority:f490a0"
    "low-priority:Nice to have:ffc0cb"
    "ring-0:Core system:7057ff"
    "ring-1:Essential dev tools:7057ff"
    "ring-2:Extended tools:7057ff"
    "ring-3:External integrations:7057ff"
    "ring-4:UI/Visualization:7057ff"
    "architect-tool:architect:* tools:0e8a16"
    "orchestrator-tool:orchestrator:* tools:0e8a16"
    "chronicler-tool:chronicler:* tools:0e8a16"
    "intelligence-tool:intel:* tools:0e8a16"
    "sprint-1:Foundation sprint:d93f0b"
    "sprint-2:Core tools sprint:d93f0b"
    "sprint-3:Extended tools sprint:d93f0b"
    "mvp:Minimum viable product:d93f0b"
    "future:Future enhancements:d93f0b"
    "in-progress:Work has started:fbca04"
    "blocked:Blocked by dependencies:fbca04"
    "ready-for-review:PR ready for review:fbca04"
    "needs-discussion:Requires team discussion:fbca04"
    "on-hold:Temporarily paused:fbca04"
    "good-first-issue:Good for newcomers:7057ff"
    "help-wanted:Extra attention needed:008672"
    "student-friendly:Suitable for students:0052cc"
    "learning-exercise:Educational purpose:5319e7"
    "needs-tests:Tests need to be added:f9d0c4"
    "breaking-change:Breaking changes:d73a4a"
)

for label in "${labels[@]}"; do
    IFS=':' read -r name description color <<< "$label"
    echo "Creating label: $name"
    gh label create "$name" --description "$description" --color "$color" --force
done

echo "Label setup complete!"
```

## Label Usage Guidelines

### For Issues

1. **Always include**:
   - One type label (enhancement, bug, etc.)
   - One priority label
   - Component/ring label if applicable

2. **Add when relevant**:
   - Sprint label for planned work
   - Tool-specific label if targeting a specific tool
   - Special labels (good-first-issue, student-friendly)

### For Pull Requests

1. **Always include**:
   - Type label matching the change
   - Component/ring label for affected areas
   - Status labels as PR progresses

2. **Add when relevant**:
   - breaking-change if API changes
   - needs-tests if tests are missing
   - ready-for-review when ready

### Examples

**Good Issue Labeling**:
```
Issue: Implement architect:decompose tool
Labels: enhancement, high-priority, ring-1, architect-tool, sprint-2
```

**Good PR Labeling**:
```
PR: Add unit tests for delegation module
Labels: test, ring-0, ready-for-review, sprint-1
```

## Maintenance

- Review labels quarterly
- Archive unused labels
- Keep descriptions updated
- Ensure new contributors understand the labeling system
- Document any label changes in team meetings

## Label Meanings for Students

### Beginner-Friendly Labels
- **good-first-issue**: Start here! Well-defined, limited scope
- **student-friendly**: Designed with learning in mind
- **documentation**: Great way to learn the codebase
- **learning-exercise**: Specifically created for education

### Progression Path
1. Start with `good-first-issue` + `documentation`
2. Move to `student-friendly` + `test`
3. Progress to `enhancement` + `low-priority`
4. Eventually tackle `high-priority` items

This labeling system helps maintain an organized, accessible project that supports both production development and educational goals.