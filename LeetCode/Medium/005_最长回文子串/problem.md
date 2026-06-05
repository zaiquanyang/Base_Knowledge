# 5. 最长回文子串

**难度:** 中等  
**标签:** 双指针, 字符串, 动态规划

**链接:** [LeetCode](https://leetcode.cn/problems/longest-palindromic-substring/)

## 题目描述

给你一个字符串 `s`，找到 `s` 中最长的 回文 子串。

 

**示例 1：**

```

**输入：**s = "babad"
**输出：**"bab"
**解释：**"aba" 同样是符合题意的答案。

```

**示例 2：**

```

**输入：**s = "cbbd"
**输出：**"bb"

```

 

**提示：**

	- `1 
	- `s` 仅由数字和英文字母组成

## 提示

1. How can we reuse a previously computed palindrome to compute a larger palindrome?
2. If “aba” is a palindrome, is “xabax” a palindrome? Similarly is “xabay” a palindrome?
3. Complexity based hint: If we use brute-force and check whether for every start and end position a substring is a palindrome we have O(n^2) start - end pairs and O(n) palindromic checks. Can we reduce the time for palindromic checks to O(1) by reusing some previous computation.
