# 54. 螺旋矩阵

**难度:** 中等  
**标签:** 数组, 矩阵, 模拟

**链接:** [LeetCode](https://leetcode.cn/problems/spiral-matrix/)

## 题目描述

给你一个 `m` 行 `n` 列的矩阵 `matrix` ，请按照 **顺时针螺旋顺序** ，返回矩阵中的所有元素。

 

**示例 1：**

```

**输入：**matrix = [[1,2,3],[4,5,6],[7,8,9]]
**输出：**[1,2,3,6,9,8,7,4,5]

```

**示例 2：**

```

**输入：**matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
**输出：**[1,2,3,4,8,12,11,10,9,5,6,7]

```

 

**提示：**

	- `m == matrix.length`
	- `n == matrix[i].length`
	- `1 
	- `-100

## 提示

1. Well for some problems, the best way really is to come up with some algorithms for simulation. Basically, you need to simulate what the problem asks us to do.
2. We go boundary by boundary and move inwards. That is the essential operation. First row, last column, last row, first column, and then we move inwards by 1 and repeat. That's all. That is all the simulation that we need.
3. Think about when you want to switch the progress on one of the indexes. If you progress on i out of [i, j], you'll shift in the same column. Similarly, by changing values for j, you'd be shifting in the same row. Also, keep track of the end of a boundary so that you can move inwards and then keep repeating. It's always best to simulate edge cases like a single column or a single row to see if anything breaks or not.
