from typing import List, Optional


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        if not board:
            return 
        
        m, n = len(board), len(board[0])

        def dfs(s, k):
            if s<0 or s>=m or k<0 or k>=n or board[s][k] != 'O':
                return
            board[s][k] = '#'

            dfs(s+1, k)
            dfs(s-1, k)
            dfs(s, k+1)
            dfs(s, k-1)
        # 从左右两边的边界开始dfs
        for s in range(m):
            dfs(s, 0)
            dfs(s, n-1)

        # 从上下两行的边界开始dfs
        for k in range(n):
            dfs(0, k)
            dfs(m-1, k)

        for s in range(m):
            for k in range(n):
                if board[s][k] == 'O':
                    board[s][k] = 'X'
                elif board[s][k] == '#':
                    board[s][k]='O'

        return board





# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
