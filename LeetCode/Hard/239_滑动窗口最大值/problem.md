# 239. 滑动窗口最大值

**难度:** 困难  
**标签:** 队列, 数组, 滑动窗口, 单调队列, 堆（优先队列）

**链接:** [LeetCode](https://leetcode.cn/problems/sliding-window-maximum/)

## 题目描述

给你一个整数数组 `nums`，有一个大小为 `k`* *的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 `k` 个数字。滑动窗口每次只向右移动一位。

返回 *滑动窗口中的最大值 *。

 

**示例 1：**

```

输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       **3**
 1 [3  -1  -3] 5  3  6  7       **3**
 1  3 [-1  -3  5] 3  6  7      ** 5**
 1  3  -1 [-3  5  3] 6  7       **5**
 1  3  -1  -3 [5  3  6] 7       **6**
 1  3  -1  -3  5 [3  6  7]      **7**

```

**示例 2：**

```

输入：nums = [1], k = 1
输出：[1]

```

 

提示：

	- `1 5`
	- `-104 4`
	- `1

## 提示

1. How about using a data structure such as deque (double-ended queue)?
2. The queue size need not be the same as the window’s size.
3. Remove redundant elements and the queue should store only elements that need to be considered.
