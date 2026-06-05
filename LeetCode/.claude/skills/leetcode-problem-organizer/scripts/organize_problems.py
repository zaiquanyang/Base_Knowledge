#!/usr/bin/env python3
"""
LeetCode Problem Organizer

Organizes fetched LeetCode problems into categorized folder structure
with problem description markdown and Python solution templates.
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any
import html


class ProblemOrganizer:
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename"""
        # Remove or replace invalid filename characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.strip()
        return filename

    def extract_python_code(self, code_snippets: List[Dict]) -> str:
        """Extract Python code snippet from code snippets list"""
        for snippet in code_snippets:
            if snippet.get('langSlug') == 'python3' or snippet.get('lang') == 'Python3':
                return snippet.get('code', '')
        # Fallback to first snippet if no Python3 found
        return code_snippets[0].get('code', '') if code_snippets else ''

    def clean_html(self, text: str) -> str:
        """Convert HTML entities and tags to readable text"""
        if not text:
            return ""
        
        # Unescape HTML entities
        text = html.unescape(text)
        
        # Remove HTML tags but keep content
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def format_examples(self, examples: List[Dict]) -> str:
        """Format examples into readable markdown"""
        if not examples:
            return ""
        
        formatted = "### Examples\n\n"
        for idx, example in enumerate(examples, 1):
            formatted += f"**Example {idx}:**\n\n"
            formatted += f"```\n"
            if 'input' in example:
                formatted += f"Input: {example['input']}\n"
            if 'output' in example:
                formatted += f"Output: {example['output']}\n"
            formatted += f"```\n"
            
            if 'explanation' in example and example['explanation']:
                formatted += f"\n**Explanation:** {self.clean_html(example['explanation'])}\n\n"
        
        return formatted

    def generate_problem_md(self, problem: Dict[str, Any]) -> str:
        """Generate markdown content for problem description"""
        md = f"# {problem['id']}. {problem['title']}\n\n"
        md += f"**Difficulty:** {problem['difficulty']}\n\n"
        
        if problem.get('category'):
            md += f"**Category:** {problem['category']}\n\n"
        
        md += "## Problem Description\n\n"
        
        # Clean and add description
        description = problem.get('description', '')
        if description:
            # Clean HTML from description
            description = self.clean_html(description)
            md += f"{description}\n\n"
        
        # Add examples
        if problem.get('examples'):
            md += self.format_examples(problem['examples'])
        
        # Add hints if available
        if problem.get('hints'):
            md += "## Hints\n\n"
            for idx, hint in enumerate(problem['hints'], 1):
                hint_text = self.clean_html(hint) if isinstance(hint, str) else hint
                md += f"{idx}. {hint_text}\n"
            md += "\n"
        
        # Add constraints if not already in description (try to extract from description)
        md += "## Constraints\n\n"
        md += "- See problem description for constraints\n"
        
        return md

    def generate_solution_py(self, problem: Dict[str, Any]) -> str:
        """Generate Python solution template"""
        # Try to extract function signature from code snippets
        code_snippet = self.extract_python_code(problem.get('code_snippets', []))
        
        if code_snippet:
            # Extract function definition
            lines = code_snippet.split('\n')
            function_lines = []
            in_function = False
            indent_level = 0
            
            for line in lines:
                if 'def ' in line and not in_function:
                    in_function = True
                    function_lines.append(line)
                elif in_function:
                    if line.strip() and not line[0].isspace() and line.strip() != '':
                        # End of function definition
                        break
                    function_lines.append(line)
            
            if function_lines:
                # Clean up and format
                code = '\n'.join(function_lines)
                # Remove the pass statement if present and keep just the signature
                code = re.sub(r'(\n\s+)pass\s*$', '', code)
                if not code.strip().endswith(':'):
                    code = code.rstrip()
                    if not code.endswith(':'):
                        code += ':'
                
                # Add placeholder
                code += "\n        \"\"\"\n        TODO: Implement solution\n        \"\"\"\n        pass\n"
                
                return f"from typing import List, Optional, Dict\n\n\n{code}\n"
        
        # Fallback template
        return f'''from typing import List, Optional, Dict


class Solution:
    def solve(self, *args, **kwargs):
        """
        TODO: Implement solution for problem {problem['id']}: {problem['title']}
        
        Refer to problem.md for detailed problem description.
        """
        pass
'''

    def create_problem_folder(self, problem: Dict[str, Any], category_dir: Path) -> None:
        """Create folder for a single problem with description and solution template"""
        # Create problem folder name: {id}_{title}
        folder_name = f"{problem['id']:03d}_{self.sanitize_filename(problem['title'])}"
        problem_dir = category_dir / folder_name
        problem_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate and save problem.md
        problem_md = self.generate_problem_md(problem)
        problem_file = problem_dir / "problem.md"
        with open(problem_file, 'w', encoding='utf-8') as f:
            f.write(problem_md)
        
        # Generate and save solution.py
        solution_py = self.generate_solution_py(problem)
        solution_file = problem_dir / "solution.py"
        with open(solution_file, 'w', encoding='utf-8') as f:
            f.write(solution_py)
        
        print(f"Created: {problem_dir}")

    def organize_problems(self, problems: List[Dict[str, Any]], organize_by: str = 'difficulty') -> None:
        """
        Organize problems into categorized folder structure
        
        organize_by: 'difficulty' or 'category'
        """
        if organize_by == 'difficulty':
            # Group by difficulty
            grouped = {'Easy': [], 'Medium': [], 'Hard': []}
            for problem in problems:
                difficulty = problem.get('difficulty', 'Medium')
                if difficulty not in grouped:
                    grouped[difficulty] = []
                grouped[difficulty].append(problem)
            
            # Create folders
            for difficulty, probs in grouped.items():
                if not probs:
                    continue
                diff_dir = self.output_dir / difficulty
                diff_dir.mkdir(parents=True, exist_ok=True)
                
                for problem in probs:
                    self.create_problem_folder(problem, diff_dir)
        
        elif organize_by == 'category':
            # Group by category
            grouped = {}
            for problem in problems:
                category = problem.get('category') or 'Other'
                if category not in grouped:
                    grouped[category] = []
                grouped[category].append(problem)
            
            # Create folders
            for category, probs in grouped.items():
                cat_dir = self.output_dir / self.sanitize_filename(category)
                cat_dir.mkdir(parents=True, exist_ok=True)
                
                for problem in probs:
                    self.create_problem_folder(problem, cat_dir)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python organize_problems.py <json_file> [output_dir] [difficulty|category]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    organize_by = sys.argv[3] if len(sys.argv) > 3 else "difficulty"
    
    # Load problems from JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        problems = json.load(f)
    
    # Organize
    organizer = ProblemOrganizer(output_dir)
    organizer.organize_problems(problems, organize_by=organize_by)
    
    print(f"\n✓ Successfully organized {len(problems)} problems!")
    print(f"Output directory: {Path(output_dir).absolute()}")


if __name__ == "__main__":
    main()
