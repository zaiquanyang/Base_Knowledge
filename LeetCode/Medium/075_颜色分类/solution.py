from typing import List, Optional


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # 利用三指针进行单次遍历，把 0 统统交换到左边，把 2 统统交换到右边，中间自然就留下了 1。
        left, current = 0, 0
        right = len(nums) - 1

        while current <= right:
            if nums[current]==0:
                nums[current], nums[left] = nums[left], nums[current]
                left += 1
                current += 1
            elif nums[current] == 1:
                current += 1
            elif nums[current] == 2:
                nums[current], nums[right] = nums[right], nums[current]
                right -= 1
        
        return nums
        


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
