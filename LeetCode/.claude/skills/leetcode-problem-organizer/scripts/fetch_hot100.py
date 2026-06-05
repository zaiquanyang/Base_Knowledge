#!/usr/bin/env python3
"""
Fetch LeetCode CN Hot 100 problems and save as JSON.
"""

import requests
import json
import time
import sys
import os

BASE_URL = "https://leetcode.cn/graphql"
HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://leetcode.cn',
}

# Known popular lists
LISTS = {
    "hot100": "2ckc81c",
    "top-interview-150": "xitmg4i",
}


def fetch_problem_list(list_slug, limit=200):
    """Fetch all problems from a favorite list."""
    query = """
    query favoriteQuestionList($favoriteSlug:String!,$limit:Int,$skip:Int){
        favoriteQuestionList(favoriteSlug:$favoriteSlug,limit:$limit,skip:$skip){
            totalLength hasMore
            questions{
                questionFrontendId title translatedTitle titleSlug difficulty
                topicTags{name slug nameTranslated}
                paidOnly
            }
        }
    }
    """
    variables = {"favoriteSlug": list_slug, "limit": limit, "skip": 0}
    resp = requests.post(BASE_URL, json={"query": query, "variables": variables}, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        print(f"GraphQL errors: {data['errors']}", file=sys.stderr)
        return []
    result = data["data"]["favoriteQuestionList"]
    return result["questions"]


def fetch_problem_detail(title_slug):
    """Fetch detailed problem info including description, examples, code snippets."""
    query = """
    query questionData($titleSlug:String!){
        question(titleSlug:$titleSlug){
            questionId questionFrontendId title translatedTitle
            difficulty content translatedContent
            exampleTestcaseList
            hints
            codeSnippets{lang langSlug code}
            topicTags{name slug translatedName}
        }
    }
    """
    variables = {"titleSlug": title_slug}
    resp = requests.post(BASE_URL, json={"query": query, "variables": variables}, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        print(f"  GraphQL errors for {title_slug}: {data['errors']}", file=sys.stderr)
        return {}
    return data.get("data", {}).get("question", {})


def main():
    list_name = sys.argv[1] if len(sys.argv) > 1 else "hot100"
    list_slug = LISTS.get(list_name, list_name)

    print(f"Fetching problem list: {list_name} (slug: {list_slug})")
    questions = fetch_problem_list(list_slug)
    print(f"Found {len(questions)} problems")

    if not questions:
        print("No problems found!")
        sys.exit(1)

    problems = []
    for idx, q in enumerate(questions, 1):
        slug = q["titleSlug"]
        title = q.get("translatedTitle") or q.get("title", "")
        print(f"[{idx}/{len(questions)}] Fetching detail: {q['questionFrontendId']} - {title}")

        detail = fetch_problem_detail(slug)
        time.sleep(0.3)  # rate limit

        # Extract tags
        tags = []
        for tag in (detail.get("topicTags") or q.get("topicTags") or []):
            tags.append(tag.get("nameTranslated") or tag.get("translatedName") or tag.get("name", ""))

        # Extract python3 code snippet
        code_snippet = ""
        for snippet in (detail.get("codeSnippets") or []):
            if snippet.get("langSlug") == "python3":
                code_snippet = snippet.get("code", "")
                break

        problem = {
            "id": q["questionFrontendId"],
            "title": title,
            "title_en": q.get("title", ""),
            "title_slug": slug,
            "difficulty": q.get("difficulty", "MEDIUM"),
            "tags": tags,
            "description": detail.get("translatedContent") or detail.get("content", ""),
            "examples": [],
            "hints": detail.get("hints") or [],
            "code_snippet": code_snippet,
            "paid_only": q.get("paidOnly", False),
        }

        # Parse examples from exampleTestcaseList or extract from content
        example_list = detail.get("exampleTestcaseList") or []
        content = detail.get("translatedContent") or detail.get("content", "")
        if content and example_list:
            # Use exampleTestcaseList paired with content extraction
            problem["examples"] = example_list

        problems.append(problem)

    # Save to JSON
    output_file = os.path.join(os.path.dirname(__file__), f"../data/{list_name}_problems.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(problems)} problems to {output_file}")


if __name__ == "__main__":
    main()
