from typing import List, Optional


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        """
        N = len(mat)
        mat[i][j]--->mat[j][N-1-i]
        mat[j][N-1-i]--->mat[N-1-i][N-1-j]
        mat[N-1-i][N-1-j]--->mat[N-1-j][i]
        mat[N-1-j][i]------> mat[i][j]
        """
        N = len(matrix)
        n = (N+1)//2
        # print(n)
        for i in range(n):
            for j in range(N-n):
                a, b, c, d = matrix[i][j], matrix[j][N-1-i], matrix[N-1-i][N-1-j], matrix[N-1-j][i]
                matrix[j][N-1-i] = a
                matrix[N-1-i][N-1-j] = b
                matrix[N-1-j][i] = c
                matrix[i][j] = d

        return matrix



# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
