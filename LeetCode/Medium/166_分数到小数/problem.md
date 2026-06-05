# 166. 分数到小数

**难度:** 中等  
**标签:** 哈希表, 数学, 字符串

**链接:** [LeetCode](https://leetcode.cn/problems/fraction-to-recurring-decimal/)

## 题目描述

给定两个整数，分别表示分数的分子 `numerator` 和分母 `denominator`，以 **字符串形式返回小数** 。

如果小数部分为循环小数，则将循环的部分括在括号内。

如果存在多个答案，只需返回 **任意一个** 。

对于所有给定的输入，**保证** 答案字符串的长度小于 `104` 。

**注意**，如果分数可以表示为有限长度的字符串，则 **必须** 返回它。

 

**示例 1：**

```

**输入：**numerator = 1, denominator = 2
**输出：**"0.5"

```

**示例 2：**

```

**输入：**numerator = 2, denominator = 1
**输出：**"2"

```

**示例 3：**

```

**输入：**numerator = 4, denominator = 333
**输出：**"0.(012)"

```

 

**提示：**

	- `-231 31 - 1`
	- `denominator != 0`

## 提示

1. No scary math, just apply elementary math knowledge. Still remember how to perform a long division?
2. Try a long division on 4/9, the repeating part is obvious. Now try 4/333. Do you see a pattern?
3. Notice that once the remainder starts repeating, so does the divided result.
4. Be wary of edge cases! List out as many test cases as you can think of and test your code thoroughly.
