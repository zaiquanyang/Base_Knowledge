---
name: leetcode-problem-organizer
description: 'Organize LeetCode problems from a problem list into categorized folders with markdown descriptions and Python solution templates. Use when: importing LeetCode problem lists, creating structured practice materials, setting up organized coding challenges by difficulty or algorithm type.'
argument-hint: 'LeetCode problem list URL (e.g., https://leetcode.cn/problem-list/2ckc81c/)'
---

# LeetCode Problem Organizer

A skill that automatically fetches LeetCode problems from a given problem list URL, categorizes them by difficulty and topic, and generates organized file structures with problem descriptions and Python solution templates.

## What It Does

1. **Fetches Problems**: Scrapes LeetCode problem data from the provided problem list
2. **Categorizes**: Organizes problems by difficulty (Easy, Medium, Hard) and algorithm topic (if available)
3. **Generates Files**:
   - `problem.md`: Problem description, examples, and test cases
   - `solution.py`: Python solution template with function signature

## When to Use

- **Setting up study material**: Convert a LeetCode problem list into a structured local repository
- **Batch problem import**: Organize multiple problems at once with consistent formatting
- **Practice preparation**: Create categorized problem sets for interview prep
- **Local development**: Work through problems with proper templates and organization

## Procedure

1. **Get the problem list URL**
   - Navigate to LeetCode (CN or global) problem list
   - Copy the URL from the address bar
   - Example: `https://leetcode.cn/problem-list/2ckc81c/`

2. **Run the Organizer**
   - Invoke the skill with the problem list URL
   - Wait for the fetching and organization process to complete

3. **Review the Generated Structure**
   - Check the output in your workspace
   - Problems are organized in folders like `Easy/`, `Medium/`, `Hard/`
   - Each problem has:
     - `problem.md` - Full problem description
     - `solution.py` - Starter template with function signature

4. **Start Solving**
   - Open any `solution.py` file in your editor
   - Implement the solution within the function template
   - Reference the `problem.md` for requirements and test cases

## Generated Structure Example

```
LeetCode/
├── Easy/
│   ├── 001_Two_Sum/
│   │   ├── problem.md
│   │   └── solution.py
│   └── 020_Valid_Parentheses/
│       ├── problem.md
│       └── solution.py
├── Medium/
│   ├── 002_Add_Two_Numbers/
│   │   ├── problem.md
│   │   └── solution.py
│   └── ...
└── Hard/
    └── ...
```

## References

- [Problem fetching script](./scripts/fetch_problems.py): Handles API calls and data parsing
- [Organization script](./scripts/organize_problems.py): Creates folder structure and files
- [Problem template](./assets/problem_template.md): Format for problem markdown files
- [Solution template](./assets/solution_template.py): Python solution starter
