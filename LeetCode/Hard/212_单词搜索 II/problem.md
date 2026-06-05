# 212. 单词搜索 II

**难度:** 困难  
**标签:** 字典树, 数组, 字符串, 回溯, 矩阵

**链接:** [LeetCode](https://leetcode.cn/problems/word-search-ii/)

## 题目描述

给定一个 `m x n` 二维字符网格 `board`** **和一个单词（字符串）列表 `words`， *返回所有二维网格上的单词* 。

单词必须按照字母顺序，通过 **相邻的单元格** 内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母在一个单词中不允许被重复使用。

 

**示例 1：**

```

**输入：**board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
**输出：**["eat","oath"]

```

**示例 2：**

```

**输入：**board = [["a","b"],["c","d"]], words = ["abcb"]
**输出：**[]

```

 

**提示：**

	- `m == board.length`
	- `n == board[i].length`
	- `1 
	- `board[i][j]` 是一个小写英文字母
	- `1 4`
	- `1 
	- `words[i]` 由小写英文字母组成
	- `words` 中的所有字符串互不相同

## 提示

1. You would need to optimize your backtracking to pass the larger test. Could you stop backtracking earlier?
2. If the current candidate does not exist in all words' prefix, you could stop backtracking immediately. What kind of data structure could answer such query efficiently? Does a hash table work? Why or why not? How about a Trie? If you would like to learn how to implement a basic trie, please work on this problem: Implement Trie (Prefix Tree) first.
