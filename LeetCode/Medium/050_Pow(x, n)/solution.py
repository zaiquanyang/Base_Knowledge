from typing import List, Optional


class Solution:
    def myPow(self, x: float, n: int) -> float:
        
        if n == 0:
            return 1
        if n < 0:
            x = 1/x
            n = -n


        def quick_pow(x, n):

            if n== 1:
                return x
            

            if n % 2 == 0:
                cur_pow = quick_pow(x, n//2)
                cur_pow = cur_pow * cur_pow
            else:
                cur_pow = quick_pow(x, n//2)
                cur_pow = cur_pow * cur_pow * x

            return cur_pow

        return quick_pow(x, n)


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
