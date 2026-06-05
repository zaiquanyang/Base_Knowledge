from typing import List, Optional


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_jump = 0

        for i in range(len(nums)):
            if i > max_jump:
                return False
            
            max_jump = max(max_jump, i+nums[i])
            if max_jump >= len(nums)-1:
                return True
        


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
