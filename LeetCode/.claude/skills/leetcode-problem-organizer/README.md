# LeetCode Problem Organizer - README

## Quick Start

This skill helps you organize LeetCode problems into a structured local repository with problem descriptions and Python solution templates.

### Prerequisites

- Python 3.7+
- `requests` library: `pip install requests`

### Usage

#### Option 1: Use the Skill Directly

In VS Code Copilot Chat:
```
/leetcode-problem-organizer https://leetcode.cn/problem-list/2ckc81c/
```

#### Option 2: Use Scripts Manually

1. **Fetch problems:**

```bash
python scripts/fetch_problems.py "https://leetcode.cn/problem-list/2ckc81c/" > problems.json
```

Or limit to first 10 problems:
```bash
python scripts/fetch_problems.py "https://leetcode.cn/problem-list/2ckc81c/" 10 > problems.json
```

2. **Organize problems:**

```bash
python scripts/organize_problems.py problems.json output_dir difficulty
```

Options for organizing:
- `difficulty` - Group by Easy/Medium/Hard
- `category` - Group by algorithm category

### Output Structure

```
output_dir/
├── Easy/
│   ├── 001_Two_Sum/
│   │   ├── problem.md
│   │   └── solution.py
│   └── 020_Valid_Parentheses/
│       ├── problem.md
│       └── solution.py
├── Medium/
│   └── ...
└── Hard/
    └── ...
```

Each problem folder contains:
- **problem.md**: Full problem description with examples, constraints, and hints
- **solution.py**: Python class with function signature and template for your solution

### Tips

1. Open `problem.md` to understand the problem completely
2. Implement your solution in `solution.py`
3. Run test cases using the template provided
4. Reference the hints when stuck

### Supported URLs

- **LeetCode China**: `https://leetcode.cn/problem-list/{LIST_ID}/`
- **LeetCode Global**: `https://leetcode.com/problem-list/{LIST_ID}/`

### Troubleshooting

**Connection issues:**
- Check your internet connection
- LeetCode API may have rate limits
- Try fetching fewer problems first

**JSON parsing errors:**
- Ensure problems.json is valid
- Try re-fetching the problems

**File encoding issues on Windows:**
- Scripts use UTF-8 encoding by default
- If you see encoding errors, check your console encoding
