#!/usr/bin/env python3
"""
LeetCode Problem Fetcher

Fetches problems from LeetCode problem lists via GraphQL API.
Supports both leetcode.com and leetcode.cn
"""

import requests
import json
import re
from typing import List, Dict, Any
from urllib.parse import urlparse


class LeetCodeFetcher:
    def __init__(self, is_cn: bool = False):
        self.is_cn = is_cn
        self.base_url = "https://leetcode.cn" if is_cn else "https://leetcode.com"
        self.api_url = f"{self.base_url}/graphql"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def extract_list_id(self, url: str) -> str:
        """Extract list ID from LeetCode problem list URL"""
        match = re.search(r'problem-list/([^/?]+)', url)
        if match:
            return match.group(1)
        raise ValueError("Invalid LeetCode problem list URL")

    def fetch_problem_list(self, list_id: str) -> List[Dict[str, Any]]:
        """Fetch all problems from a problem list"""
        query = """
        query getProblemList($listId: String!) {
            problemsetQuestionList(listId: $listId, limit: 1000, skip: 0) {
                data {
                    questions {
                        id
                        questionId
                        title
                        titleCn
                        titleSlug
                        difficulty
                        status
                        paidOnly
                        categoryTitle
                        categoryTitleCn
                    }
                }
            }
        }
        """
        
        variables = {"listId": list_id}
        
        try:
            response = self.session.post(
                self.api_url,
                json={"query": query, "variables": variables},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                raise Exception(f"GraphQL Error: {data['errors']}")
            
            questions = data.get("data", {}).get("problemsetQuestionList", {}).get("data", {}).get("questions", [])
            return questions
        except Exception as e:
            print(f"Error fetching problem list: {e}")
            return []

    def fetch_problem_detail(self, title_slug: str) -> Dict[str, Any]:
        """Fetch detailed problem information"""
        query = """
        query getProblemDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleCn
                difficulty
                content
                contentCn
                examples {
                    input
                    output
                    explanation
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                hints
                exampleTestcaseList
            }
        }
        """
        
        variables = {"titleSlug": title_slug}
        
        try:
            response = self.session.post(
                self.api_url,
                json={"query": query, "variables": variables},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                raise Exception(f"GraphQL Error: {data['errors']}")
            
            return data.get("data", {}).get("question", {})
        except Exception as e:
            print(f"Error fetching problem detail for {title_slug}: {e}")
            return {}

    def fetch_all_problems(self, list_url: str, max_problems: int = None) -> List[Dict[str, Any]]:
        """Fetch all problems with details from a problem list URL"""
        list_id = self.extract_list_id(list_url)
        print(f"Fetching problems from list ID: {list_id}")
        
        # Get problem list
        questions = self.fetch_problem_list(list_id)
        print(f"Found {len(questions)} problems")
        
        if max_problems:
            questions = questions[:max_problems]
        
        # Get detailed information for each problem
        problems = []
        for idx, q in enumerate(questions, 1):
            print(f"Fetching details for problem {idx}/{len(questions)}: {q.get('title', q.get('titleCn', 'N/A'))}")
            detail = self.fetch_problem_detail(q['titleSlug'])
            
            problem = {
                'id': q.get('questionId'),
                'title': q.get('titleCn') or q.get('title'),
                'title_slug': q.get('titleSlug'),
                'difficulty': q.get('difficulty'),
                'category': q.get('categoryTitleCn') or q.get('categoryTitle'),
                'description': detail.get('contentCn') or detail.get('content'),
                'examples': detail.get('examples', []),
                'code_snippets': detail.get('codeSnippets', []),
                'hints': detail.get('hints', []),
            }
            problems.append(problem)
        
        return problems


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python fetch_problems.py <leetcode_url> [max_problems]")
        sys.exit(1)
    
    url = sys.argv[1]
    max_problems = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    # Detect if it's CN version
    is_cn = "leetcode.cn" in url
    
    fetcher = LeetCodeFetcher(is_cn=is_cn)
    problems = fetcher.fetch_all_problems(url, max_problems=max_problems)
    
    # Output as JSON
    print(json.dumps(problems, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
