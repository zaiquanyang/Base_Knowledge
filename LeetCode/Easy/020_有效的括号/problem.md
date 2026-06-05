# 20. 有效的括号

**难度:** 简单  
**标签:** 栈, 字符串

**链接:** [LeetCode](https://leetcode.cn/problems/valid-parentheses/)

## 题目描述

给定一个只包括 `'('`，`')'`，`'{'`，`'}'`，`'['`，`']'` 的字符串 `s` ，判断字符串是否有效。

有效字符串需满足：

	- 左括号必须用相同类型的右括号闭合。
	- 左括号必须以正确的顺序闭合。
	- 每个右括号都有一个对应的相同类型的左括号。

 

示例 1：

输入：s = "()"

输出：true

示例 2：

输入：s = "()[]{}"

输出：true

示例 3：

输入：s = "(]"

输出：false

示例 4：

输入：s = "([])"

输出：true

示例 5：

输入：s = "([)]"

输出：false

 

**提示：**

	- `1 4`
	- `s` 仅由括号 `'()[]{}'` 组成

## 提示

1. Use a stack of characters.
2. When you encounter an opening bracket, push it to the top of the stack.
3. When you encounter a closing bracket, check if the top of the stack was the opening for it. If yes, pop it from the stack. Otherwise, return false.
