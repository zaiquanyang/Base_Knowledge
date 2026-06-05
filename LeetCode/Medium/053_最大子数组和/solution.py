from typing import List, Optional


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]
        cur_max_sum = nums[0]
        N = len(nums)

        for i in range(1, N):
            cur_max_sum = max(nums[i], nums[i]+cur_max_sum)

            max_sum = max(cur_max_sum, max_sum)
        
        return max_sum



# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
