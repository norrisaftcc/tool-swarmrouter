# 🐝 HIVE Contributor Guide Module

## Overview

The Contributor Guide is a specialized HIVE module that helps developers (and students) navigate the contribution process for any repository. It acts as an intelligent mentor, breaking down the overwhelming "where do I start?" question into manageable steps.

## Module Design

```python
class ContributorGuideModule(HiveModule):
    """Ring 2 module that guides contributors through the OSS contribution process"""
    
    def __init__(self):
        super().__init__(ring_level=2)
        self.dependencies = ["architect_tools", "orchestrator_tools", "github_integration"]
        self.provided_tools = [
            "guide:analyze_repo",
            "guide:find_good_first_issues", 
            "guide:create_learning_path",
            "guide:pair_on_issue",
            "guide:review_pr_together"
        ]
```

## User Experience Flow

### 1. Initial Repository Analysis

```
User: "I want to contribute to kubernetes/minikube but don't know where to start"

🐝 HIVE Contributor Guide:
Let me analyze this repository and create a personalized contribution path for you...

[Dancing bees animation while analyzing]

## Repository Analysis: kubernetes/minikube

### 📊 Repository Stats
- Stars: 27.5k ⭐
- Contributors: 736
- Open Issues: 459
- Good First Issues: 12 
- Primary Language: Go (71.2%)
- Activity Level: Very High (50+ commits/week)

### 🎯 Contribution Difficulty: Medium-High
- Requires Go knowledge
- Complex codebase
- Active maintenance
- Welcoming community

### 🐝 Your Personalized Path
Based on your GitHub profile, I've created this learning path:

1. **Setup Phase** (Week 1)
   - [ ] Fork and clone repository
   - [ ] Set up Go development environment
   - [ ] Run minikube locally
   - [ ] Read CONTRIBUTING.md

2. **Learning Phase** (Week 2-3)
   - [ ] Complete Go tour (you haven't used Go before)
   - [ ] Study minikube architecture docs
   - [ ] Run the test suite
   - [ ] Join #minikube-dev Slack channel

3. **First Contribution** (Week 4)
   - [ ] I found 3 suitable "good first issues"
   - [ ] Let's pair on understanding one together
   - [ ] Submit your first PR!

Would you like me to guide you through Step 1 now?
```

### 2. Interactive Issue Selection

```
User: "Show me the good first issues"

🐝 HIVE Contributor Guide:
I've analyzed the open issues and ranked them by suitability for you:

## 🎯 Recommended First Issues

### 1. [IDEAL] Update error message in start command
- **Why this is perfect**: Simple string change, great for learning the workflow
- **Skills needed**: Basic Go, Git
- **Estimated time**: 2-3 hours
- **Competition**: Low (created 2 days ago)
- 🐝 **Bee Assessment**: "This is your honey pot! Perfect starter issue."

### 2. [GOOD] Add unit test for config validation
- **Why this suits you**: You have testing experience from your Python projects
- **Skills needed**: Go testing framework, understanding of config module
- **Estimated time**: 4-6 hours  
- **Competition**: Medium (1 person expressed interest)
- 🐝 **Bee Assessment**: "Slightly more complex but builds on your testing knowledge."

### 3. [STRETCH] Fix shell completion for fish shell
- **Why consider this**: Unique issue, less competition
- **Skills needed**: Shell scripting, fish shell knowledge
- **Estimated time**: 6-8 hours
- **Competition**: None
- 🐝 **Bee Assessment**: "A challenge, but you'd learn a lot!"

### 🚫 Issues to Avoid (for now)
- #15234: Requires deep Kubernetes knowledge
- #15190: Performance optimization (needs profiling skills)
- #15203: Already has 3 people working on it

Shall we do a deep dive on Issue #1 together?
```

### 3. Collaborative Issue Understanding

```
User: "Yes, let's look at issue #1"

🐝 HIVE Contributor Guide:
Excellent choice! Let's break this down together:

## 📋 Issue #15245: Update error message in start command

### Original Issue
```
When running `minikube start` with an invalid driver, the error message says:
"Invalid driver: %s"

This should be more helpful and suggest valid drivers.
```

### 🐝 Let's Understand This Together

**Step 1: Find where this happens**
I'll search the codebase with you...

Found it! The error is in `/cmd/minikube/cmd/start.go` line 234:
```go
return fmt.Errorf("Invalid driver: %s", driverName)
```

**Step 2: Understand the context**
This function validates the driver before starting. Valid drivers are:
- docker
- virtualbox  
- hyperkit
- kvm2
- none

**Step 3: Plan the fix**
We should change it to:
```go
return fmt.Errorf("Invalid driver: %s. Valid drivers are: %s", 
    driverName, strings.Join(validDrivers, ", "))
```

### 🎯 Your Action Plan
1. Create a branch: `fix/helpful-driver-error-message`
2. Make the change in start.go
3. Update the test in start_test.go
4. Run: `make test`
5. Commit with message: "fix(start): improve invalid driver error message"

Would you like me to:
A) 👥 Pair with you through the implementation
B) 📝 Create a PR template for you
C) 🧪 Help you write the test
```

### 4. Group Learning Mode

```
User: "Actually, I'm doing this with my study group"

🐝 HIVE Contributor Guide:
Wonderful! Group contributions are fantastic for learning. Let me set up a collaborative workflow:

## 👥 Group Contribution Mode Activated!

### Role Assignment (3-4 people work best)
I'll help you organize your group:

**Role 1: The Navigator** 🧭
- Reads and understands the issue
- Finds the relevant code
- Explains the problem to others

**Role 2: The Driver** ⌨️
- Makes the actual code changes
- Shares screen during coding
- Commits with co-author tags

**Role 3: The Tester** 🧪
- Writes/updates tests
- Runs the test suite
- Verifies the fix works

**Role 4: The Documenter** 📝
- Takes notes on the process
- Writes the PR description
- Updates any relevant docs

### 🐝 Collaborative Workflow

**Phase 1: Issue Analysis (30 min)**
Everyone reads the issue together. I'll provide:
- Guided questions to discuss
- Code locations to explore
- Context about the project

**Phase 2: Solution Design (20 min)**
- Discuss possible approaches
- I'll validate your ideas
- Agree on implementation plan

**Phase 3: Implementation (45 min)**
- Driver codes while others watch/help
- Rotate roles every 15 minutes
- I'll provide hints if you get stuck

**Phase 4: Review & Submit (30 min)**
- Review the changes together
- Run tests together
- Submit PR with all co-authors

### 🎓 Learning Objectives
By the end, everyone will understand:
- [ ] How to navigate a large codebase
- [ ] Git collaboration with co-authors
- [ ] The PR process from start to finish
- [ ] How to write good commit messages
- [ ] Test-driven development basics

Shall I create a shared workspace for your group?
```

### 5. PR Review Learning

```
User: "Our PR got reviewed! Help us understand the feedback"

🐝 HIVE Contributor Guide:
Great job on submitting! Let's decode this review together:

## 📝 PR Review Analysis

### Reviewer Comment 1:
> "Thanks for the PR! Could you also update the error message in the 
> validateDriver function on line 456?"

**🐝 Translation**: 
- This is positive! They said "thanks"
- They found another place with the same issue
- This is common - fixes often need to be applied in multiple places

**What to do**:
1. Search for all instances of "Invalid driver"
2. Update them all consistently
3. Reply: "Good catch! I've updated all instances of the error message."

### Reviewer Comment 2:
> "Please run `make lint` and fix any issues"

**🐝 Translation**:
- Automated linting failed
- This is routine, not criticism
- Every project has style rules

**What to do**:
```bash
make lint
# Fix any issues shown
git add -u
git commit -m "fix: address linting issues"
git push
```

### Reviewer Comment 3:
> "LGTM after the above changes"

**🐝 Translation**:
- "Looks Good To Me" 
- They'll approve after you make changes
- You're almost there! 🎉

### 📚 Review Response Template
```markdown
@reviewer Thanks for the review! I've addressed all your comments:

- ✅ Updated error message in validateDriver function
- ✅ Fixed all linting issues
- ✅ Verified all tests still pass

Please take another look when you have a chance.
```

### 🎯 Next Steps
1. Make the requested changes
2. Push to your branch
3. Comment that you've addressed feedback
4. Wait for re-review (usually 1-2 days)

Remember: Reviews are learning opportunities, not criticism!
```

## Module Implementation

```python
class ContributorGuideModule(HiveModule):
    """Guides contributors through the OSS contribution process"""
    
    async def analyze_repo(self, repo_url: str, user_profile: Dict) -> Dict:
        """Analyze repository and create personalized contribution plan"""
        
        # Use architect:decompose to understand repo structure
        repo_analysis = await self.architect.decompose({
            "input": f"Analyze repository {repo_url} for contribution suitability",
            "constraints": {
                "user_experience": user_profile["experience_level"],
                "languages": user_profile["known_languages"],
                "time_available": user_profile["time_commitment"]
            }
        })
        
        # Use intel:analyze to find patterns
        contribution_patterns = await self.intel.analyze({
            "repo": repo_url,
            "find": ["good_first_issues", "active_maintainers", "response_times"]
        })
        
        # Create personalized path
        learning_path = await self.orchestrator.plan_sprint({
            "tasks": self._generate_learning_tasks(repo_analysis),
            "velocity": user_profile["learning_speed"],
            "optimize_for": "gradual_complexity"
        })
        
        return {
            "repo_analysis": repo_analysis,
            "difficulty_rating": self._calculate_difficulty(repo_analysis),
            "personalized_path": learning_path,
            "recommended_issues": contribution_patterns["good_first_issues"][:5]
        }
        
    async def pair_on_issue(self, issue: Dict, user_context: Dict) -> AsyncIterator[str]:
        """Interactive pairing session on an issue"""
        
        yield "🐝 Let's understand this issue together!\n"
        
        # Break down the issue
        breakdown = await self.architect.decompose({
            "input": issue["description"],
            "constraints": {"explain_for": user_context["experience_level"]}
        })
        
        yield f"## Issue Breakdown\n{breakdown}\n"
        
        # Find relevant code
        yield "🔍 Searching for relevant code...\n"
        
        code_locations = await self.intel.find_code({
            "error_message": issue["error_string"],
            "likely_files": issue["component"]
        })
        
        for location in code_locations:
            yield f"Found: {location['file']}:{location['line']}\n"
            yield f"```{location['language']}\n{location['context']}\n```\n"
            
        # Suggest implementation
        implementation = await self.architect.design_solution({
            "problem": issue["description"],
            "context": code_locations,
            "constraints": ["minimal_change", "maintain_compatibility"]
        })
        
        yield f"\n## Suggested Approach\n{implementation}\n"
        
        # Create action plan
        yield "\n## Your Action Plan\n"
        for i, step in enumerate(implementation["steps"], 1):
            yield f"{i}. {step}\n"
            
    async def review_pr_together(self, pr_url: str, is_author: bool) -> Dict:
        """Help understand PR feedback"""
        
        pr_data = await self.github.get_pr(pr_url)
        reviews = await self.github.get_reviews(pr_url)
        
        if is_author:
            # Help understand feedback received
            return await self._analyze_feedback_received(reviews)
        else:
            # Help provide good feedback
            return await self._guide_review_process(pr_data)
            
    def _generate_learning_tasks(self, repo_analysis: Dict) -> List[Dict]:
        """Generate personalized learning tasks"""
        tasks = []
        
        # Always start with setup
        tasks.append({
            "name": "Environment Setup",
            "subtasks": [
                "Fork and clone repository",
                f"Install {repo_analysis['primary_language']} development environment",
                "Run project locally",
                "Read CONTRIBUTING.md"
            ],
            "estimated_hours": 4
        })
        
        # Add language learning if needed
        if repo_analysis["language_familiarity"] < 0.3:
            tasks.append({
                "name": f"Learn {repo_analysis['primary_language']} Basics",
                "subtasks": self._get_language_resources(repo_analysis['primary_language']),
                "estimated_hours": 20
            })
            
        return tasks
```

## Integration with Education

### For Instructors

```python
class ClassroomModeExtension:
    """Extensions for classroom use"""
    
    async def create_class_assignment(self, repo_url: str, class_size: int) -> Dict:
        """Create assignments for entire class"""
        
        # Find enough issues for everyone
        issues = await self.guide.find_good_first_issues(
            repo_url, 
            count=class_size * 2  # Have backups
        )
        
        # Group by difficulty
        grouped = self._group_by_difficulty(issues)
        
        # Create pairings
        assignments = self._create_pair_assignments(grouped, class_size)
        
        return {
            "assignments": assignments,
            "shared_resources": self._create_class_resources(repo_url),
            "checkpoints": self._create_learning_checkpoints()
        }
        
    async def monitor_class_progress(self, assignment_id: str) -> Dashboard:
        """Real-time dashboard of class progress"""
        
        # Track each group's progress
        progress = await self._get_group_progress(assignment_id)
        
        # Identify groups needing help
        struggling = self._identify_struggling_groups(progress)
        
        # Generate interventions
        interventions = await self._suggest_interventions(struggling)
        
        return Dashboard(progress, interventions)
```

## Benefits

1. **Reduces Intimidation**: Breaks down overwhelming repos into manageable steps
2. **Personalized Learning**: Adapts to individual skill levels
3. **Group Collaboration**: Supports team learning
4. **Real Mentorship**: Like having an experienced dev guide you
5. **Success Metrics**: Tracks contribution success rate

## Future Enhancements

1. **Reputation Building**: Track successful contributions
2. **Skill Badges**: Award badges for different types of contributions  
3. **Mentor Matching**: Connect with human mentors
4. **Project Recommendations**: Suggest next repos based on interests
5. **Conference Talk Generator**: Help create talks about contributions

This module embodies the HIVE philosophy: making complex development tasks accessible through intelligent guidance and collaborative learning!