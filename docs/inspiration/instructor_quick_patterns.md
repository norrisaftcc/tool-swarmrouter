# MCP Power Patterns: Quick Reference for Instructors

## Pattern 1: Assignment Factory
**Input**: Learning objective → **Output**: Complete assignment package

```python
async function createAssignment(learning_objective):
    # 1. Decompose into skills
    skills = await decompose_learning_query(objective, style="exploratory")
    
    # 2. Research current practices  
    examples = await web_search(f"{topic} real world examples 2025")
    
    # 3. Generate creative project
    idea = await ai_assisted_planning({
        objective: f"Create {topic} project",
        constraints: ["student_level", "time_limit", "tools_available"]
    })
    
    # 4. Design solution
    solution = await create_reasoning_chain(idea, style="deductive")
    
    # 5. Build starter code
    await filesystem.create_directory(project_structure)
    code = await artifacts.create("starter_code", solution)
    
    # 6. Generate tests
    tests = await analysis_tool(generate_test_cases(code))
    
    # 7. Package everything
    await effect_docs.generate_living_docs("assignment")
```

## Pattern 2: Sprint Planner
**Input**: Course timeline → **Output**: Agile teaching sprints

```python
async function planCourseSprints(semester_weeks, topics):
    # 1. Map topics to learning objectives
    workflow = await plan_meshnet_workflow(topics, "learning_outcome")
    
    # 2. Check institutional requirements
    requirements = await google_drive_search("department learning outcomes")
    
    # 3. Create sprint structure
    sprints = await orchestrate_educational_workflow({
        goals: topics,
        complexity: "progressive",
        time: semester_weeks * 5  # days
    })
    
    # 4. Balance workload
    balanced = await coordinate_meshnet_task({
        tasks: sprints,
        required_capabilities: ["lectures", "labs", "assignments"],
        parallelization: true
    })
    
    # 5. Document sprint plan
    await document_progress("Sprint Planning", sprints)
```

## Pattern 3: Debugging Dojo Builder
**Input**: Common error → **Output**: Interactive debugging lesson

```python
async function createDebuggingLesson(error_type):
    # 1. Understand the error deeply
    understanding = await create_reasoning_chain(
        f"Why does {error_type} occur?",
        reasoning_style: "inductive"
    )
    
    # 2. Find authoritative documentation
    docs = await scout.get_library_docs(
        language,
        topic: error_type
    )
    
    # 3. Create minimal reproduction
    repro = await artifacts.create({
        type: "code",
        content: minimal_error_example
    })
    
    # 4. Design teaching sequence
    lesson = await decompose_learning_query(
        "How to debug " + error_type,
        style: "socratic"
    )
    
    # 5. Build interactive demo
    demo = await analysis_tool(`
        // Visualize the error happening
        createErrorVisualization('${error_type}')
    `)
    
    # 6. Add to error library
    await document_progress("Debugging Library", lesson)
```

## Pattern 4: Project Scaffolder
**Input**: Project concept → **Output**: Complete project structure

```python
async function scaffoldProject(concept, student_level):
    # 1. Generate architecture
    architecture = await ai_assisted_planning({
        objective: f"Design {concept} architecture",
        constraints: [student_level, "educational_clarity"]
    })
    
    # 2. Create file structure
    for (dir of architecture.directories) {
        await filesystem.create_directory(dir)
    }
    
    # 3. Generate boilerplate with teaching comments
    for (file of architecture.files) {
        content = generateEducationalBoilerplate(file)
        await filesystem.write_file(file.path, content)
    }
    
    # 4. Add example implementations
    examples = await web_search(f"{concept} tutorial examples")
    await adaptExamplesForTeaching(examples)
    
    # 5. Create README with learning path
    readme = await generate_living_docs({
        doc_type: "workflow",
        include_learning_objectives: true
    })
```

## Pattern 5: Rapid Feedback Analyzer
**Input**: Student submissions → **Output**: Targeted improvements

```python
async function analyzeSubmissions(assignment_id):
    # 1. Gather all submissions
    submissions = await google_drive_search(
        f"assignment:{assignment_id} type:code"
    )
    
    # 2. Identify common patterns
    patterns = await track_thinking_process(
        submissions,
        look_for: ["errors", "misconceptions", "elegant_solutions"]
    )
    
    # 3. Find improvement opportunities
    synergies = await discover_synergies(
        "student_struggles",
        "course_concepts"
    )
    
    # 4. Generate targeted exercises
    exercises = await adaptive_task_routing({
        task_type: "remedial_practice",
        student_needs: patterns.struggles
    })
    
    # 5. Update course materials
    await monitor_workflow_health(
        "course_materials",
        auto_optimize: true
    )
```

## Quick Combinations for Common Tasks

### "I need a lab for tomorrow"
```
1. scout → get latest framework docs
2. artifacts → create lab handout
3. filesystem → generate starter files
4. analysis → test the lab yourself
```

### "Students struggling with concept X"  
```
1. decompose_learning_query → break it down
2. web_search → find analogies
3. artifacts → create visualization
4. document_progress → save for next time
```

### "Grading 50 submissions"
```
1. filesystem → batch read submissions
2. analysis → run automated tests
3. create_reasoning_chain → grade edge cases
4. effect_docs → generate feedback
```

### "Planning next semester"
```
1. google_drive → last semester feedback
2. track_thinking_process → identify patterns
3. orchestrate_workflow → design improvements
4. generate_living_docs → update syllabus
```

## Remember: The Magic is in the Combination

Each tool is powerful alone, but the real magic happens when you chain them together. Think of yourself as a conductor, orchestrating these tools to create educational experiences that would take weeks to build manually.

The best part? Every time you use these patterns, you can use `document_progress` to capture what worked, building an ever-improving teaching machine.