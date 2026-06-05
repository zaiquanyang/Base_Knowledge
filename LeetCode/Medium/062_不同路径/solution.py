from typing import List, Optional


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # 动态规划：到达 [i][j]位置只能从[i-1][j]和[i][j-1]位置过来，因此
        # dp[i][j] = dp[i-1][j] + dp[i][j-1], 而且 dp[0][:] = 1, dp[:][0] = 1

        dp = [[0] * n for i in range(m)]

        for i in range(m):
            dp[i][0] = 1
        for j in range(n):
            dp[0][j] = 1

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        return max([max(dp[i]) for i in range(m)])
        



# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
