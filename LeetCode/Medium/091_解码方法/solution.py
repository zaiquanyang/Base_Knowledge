from typing import List, Optional


class Solution:
    def numDecodings(self, s: str) -> int:
        if s[0] == '0':
            return 0
        # 动态规划， dp[i] = dp[i-1] + dp[i-2], dp[i] 表示前 i 个字符串的切割方法
        n = len(s)
        dp = [0] * (n+1)

        dp[0] = 1
        dp[1] = 1
        for i in range(2, n+1):
            # 最后一个字符串单独映射
            if s[i-1]!='0':
                dp[i] += dp[i-1]
            
            # 最后两个字符串一起映射
            if 10<=int(s[i-2:i])<=26:
                dp[i] += dp[i-2]
        # print(dp)
        return dp[n]



# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
