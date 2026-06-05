# 38. 外观数列

**难度:** 中等  
**标签:** 字符串

**链接:** [LeetCode](https://leetcode.cn/problems/count-and-say/)

## 题目描述

「外观数列」是一个数位字符串序列，由递归公式定义：

	- `countAndSay(1) = "1"`
	- `countAndSay(n)` 是 `countAndSay(n-1)` 的行程长度编码。

 

行程长度编码（RLE）是一种字符串压缩方法，其工作原理是通过将连续相同字符（重复两次或更多次）替换为字符重复次数（运行长度）和字符的串联。例如，要压缩字符串 `"3322251"` ，我们将 `"33"` 用 `"23"` 替换，将 `"222"` 用 `"32"` 替换，将 `"5"` 用 `"15"` 替换并将 `"1"` 用 `"11"` 替换。因此压缩后字符串变为 `"23321511"`。

给定一个整数 `n` ，返回 **外观数列** 的第 `n` 个元素。

**示例 1：**

**输入：**n = 4

**输出：**"1211"

**解释：**

countAndSay(1) = "1"

countAndSay(2) = "1" 的行程长度编码 = "11"

countAndSay(3) = "11" 的行程长度编码 = "21"

countAndSay(4) = "21" 的行程长度编码 = "1211"

示例 2：

**输入：**n = 1

**输出：**"1"

**解释：**

这是基本情况。

 

**提示：**

	- `1 

 

**进阶：**你能迭代解决该问题吗？

## 提示

1. Create a helper function that maps an integer to pairs of its digits and their frequencies. For example, if you call this function with "223314444411", then it maps it to an array of pairs [[2,2], [3,2], [1,1], [4,5], [1, 2]].
2. Create another helper function that takes the array of pairs and creates a new integer. For example, if you call this function with [[2,2], [3,2], [1,1], [4,5], [1, 2]], it should create "22"+"23"+"11"+"54"+"21" = "2223115421".
3. Now, with the two helper functions, you can start with "1" and call the two functions alternatively n-1 times. The answer is the last integer you will obtain.
