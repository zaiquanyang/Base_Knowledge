from typing import List, Optional


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        
        first_row_zero, first_col_zero = False, False
        m, n = len(matrix), len(matrix[0])

        # 先检查第一行和第一列是否包含零元素，分别设置 first_row_zero, first_col_zero
        for i in range(m):
            if matrix[i][0] == 0:
                first_col_zero = True
                break
        
        for j in range(n):
            if matrix[0][j] == 0:
                first_row_zero = True
                break
        
        # 开始遍历其他行其他列是否存在零元素，如果 matrix[i][j] == 0, 则 matrix[i][0]和matrix[0][j]都设置为0，
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[0][j] = 0
                    matrix[i][0] = 0
        # 遍历完成后，再根据首行和首列的元素值，将某些行或者列元素置0，
        for i in range(1, m):
            if matrix[i][0] == 0:
                for j in range(1, n):
                    matrix[i][j] = 0
        for j in range(1, n):
            if matrix[0][j] == 0:
                for i in range(1, m):
                    matrix[i][j] = 0
        
        # 最后再根据第一步的 first_row_zero, first_col_zero 选择是否要将首行首列置0
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0
        if first_row_zero:
            for j in range(n):
                matrix[0][j] = 0
        
        return matrix
        



# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
