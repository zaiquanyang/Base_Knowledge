# 73. 矩阵置零

**难度:** 中等  
**标签:** 数组, 哈希表, 矩阵

**链接:** [LeetCode](https://leetcode.cn/problems/set-matrix-zeroes/)

## 题目描述

给定一个 `*m* x *n*` 的矩阵，如果一个元素为 **0 **，则将其所在行和列的所有元素都设为 **0** 。请使用 **原地** 算法**。**

 

**示例 1：**

```

**输入：**matrix = [[1,1,1],[1,0,1],[1,1,1]]
**输出：**[[1,0,1],[0,0,0],[1,0,1]]

```

**示例 2：**

```

**输入：**matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
**输出：**[[0,0,0,0],[0,4,5,0],[0,3,1,0]]

```

 

**提示：**

	- `m == matrix.length`
	- `n == matrix[0].length`
	- `1 
	- `-231 31 - 1`

 

**进阶：**

	- 一个直观的解决方案是使用  `O(*m**n*)` 的额外空间，但这并不是一个好的解决方案。
	- 一个简单的改进方案是使用 `O(*m* + *n*)` 的额外空间，但这仍然不是最好的解决方案。
	- 你能想出一个仅使用常量空间的解决方案吗？

## 提示

1. If any cell of the matrix has a zero we can record its row and column number using additional memory. But if you don't want to use extra memory then you can manipulate the array instead. i.e. simulating exactly what the question says.
2. Setting cell values to zero on the fly while iterating might lead to discrepancies. What if you use some other integer value as your marker? There is still a better approach for this problem with O(1) space.
3. We could have used 2 sets to keep a record of rows/columns which need to be set to zero. But for an O(1) space solution, you can use one of the rows and and one of the columns to keep track of this information.
4. We can use the first cell of every row and column as a flag. This flag would determine whether a row or column has been set to zero.
