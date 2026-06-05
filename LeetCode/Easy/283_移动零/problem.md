# 283. 移动零

**难度:** 简单  
**标签:** 数组, 双指针

**链接:** [LeetCode](https://leetcode.cn/problems/move-zeroes/)

## 题目描述

给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序。

**请注意** ，必须在不复制数组的情况下原地对数组进行操作。

 

**示例 1:**

```

**输入:** nums = `[0,1,0,3,12]`
**输出:** `[1,3,12,0,0]`

```

**示例 2:**

```

**输入:** nums = `[0]`
**输出:** `[0]`
```

 

**提示**:

	- `1 4`
	- `-231 31 - 1`

 

进阶：你能尽量减少完成的操作次数吗？

## 提示

1. In-place means we should not be allocating any space for extra array. But we are allowed to modify the existing array. However, as a first step, try coming up with a solution that makes use of additional space. For this problem as well, first apply the idea discussed using an additional array and the in-place solution will pop up eventually.
2. A two-pointer approach could be helpful here. The idea would be to have one pointer for iterating the array and another pointer that just works on the non-zero elements of the array.
