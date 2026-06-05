#!/usr/bin/env python3
"""
Organize fetched LeetCode problems into categorized folder structure.
Adapted for the fetch_hot100.py output format.
"""

import json
import os
import re
import sys
import html as html_module
from pathlib import Path


def clean_html(text):
    """Convert HTML to readable text."""
    if not text:
        return ""
    text = html_module.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_html_multiline(text):
    """Convert HTML to readable markdown with preserved structure."""
    if not text:
        return ""
    text = html_module.unescape(text)
    # Convert common HTML tags
    text = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', text, flags=re.DOTALL)
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text)
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<li>', r'- ', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def generate_problem_md(problem):
    """Generate markdown content for problem description."""
    difficulty_cn = {"EASY": "简单", "MEDIUM": "中等", "HARD": "困难"}
    diff = difficulty_cn.get(problem['difficulty'], problem['difficulty'])

    md = f"# {problem['id']}. {problem['title']}\n\n"
    md += f"**难度:** {diff}  \n"

    if problem.get('tags'):
        md += f"**标签:** {', '.join(problem['tags'])}\n"

    md += f"\n**链接:** [LeetCode](https://leetcode.cn/problems/{problem['title_slug']}/)\n"

    md += "\n## 题目描述\n\n"
    md += clean_html_multiline(problem.get('description', '')) + "\n"

    if problem.get('hints'):
        md += "\n## 提示\n\n"
        for idx, hint in enumerate(problem['hints'], 1):
            md += f"{idx}. {clean_html(hint)}\n"

    return md


def generate_solution_py(problem):
    """Generate Python solution template."""
    code = problem.get('code_snippet', '')

    if code:
        lines = code.split('\n')
        func_lines = []
        in_func = False
        for line in lines:
            if 'def ' in line and not in_func:
                in_func = True
                func_lines.append(line)
            elif in_func:
                if line.strip() and not line[0].isspace():
                    break
                func_lines.append(line)

        if func_lines:
            code = '\n'.join(func_lines)
            # Remove trailing pass
            code = re.sub(r'\n\s+pass\s*$', '', code)
            if not code.rstrip().endswith(':'):
                code = code.rstrip()
            code += "\n        # TODO: 在此实现解题逻辑\n        pass\n"
            return f"from typing import List, Optional\n\n\nclass Solution:\n{code}\n\n\n# 测试\nif __name__ == \"__main__\":\n    sol = Solution()\n    # TODO: 添加测试用例\n    pass\n"

    return f'''from typing import List, Optional


class Solution:
    def solve(self):
        """
        {problem['id']}. {problem['title']}
        TODO: 在此实现解题逻辑
        """
        pass


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
'''


def main():
    json_file = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    organize_by = sys.argv[3] if len(sys.argv) > 3 else "difficulty"

    if not json_file:
        # Auto-find the latest JSON file
        data_dir = Path(__file__).parent.parent / "data"
        if data_dir.exists():
            json_files = sorted(data_dir.glob("*_problems.json"))
            if json_files:
                json_file = str(json_files[-1])

    if not json_file or not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        sys.exit(1)

    with open(json_file, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    print(f"Loaded {len(problems)} problems from {json_file}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if organize_by == "difficulty":
        groups = {"Easy": [], "Medium": [], "Hard": []}
        diff_map = {"EASY": "Easy", "MEDIUM": "Medium", "HARD": "Hard"}
        for p in problems:
            key = diff_map.get(p['difficulty'], "Medium")
            groups[key].append(p)
    else:
        groups = {"All": problems}

    total = 0
    for group_name, group_problems in groups.items():
        if not group_problems:
            continue
        group_dir = output_path / group_name
        group_dir.mkdir(parents=True, exist_ok=True)

        for p in group_problems:
            folder_name = f"{int(p['id']):03d}_{re.sub(r'[<>:\"/\\\\|?*]', '', p['title']).strip()}"
            problem_dir = group_dir / folder_name
            problem_dir.mkdir(parents=True, exist_ok=True)

            # Write problem.md
            with open(problem_dir / "problem.md", 'w', encoding='utf-8') as f:
                f.write(generate_problem_md(p))

            # Write solution.py
            with open(problem_dir / "solution.py", 'w', encoding='utf-8') as f:
                f.write(generate_solution_py(p))

            total += 1
            print(f"  Created: {group_name}/{folder_name}")

    print(f"\nDone! Organized {total} problems into {output_path.absolute()}")


if __name__ == "__main__":
    main()
