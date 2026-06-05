from typing import List, Optional


class Solution:
    def maxArea(self, height: List[int]) -> int:
        # 核心思路是双指针，每次只移动较短的那个指针，因为移动高的指针，面积不会变大（容器高度取决于短板）
        N = len(height)
        left, right = 0, N-1
        max_area = 0
        while left < right:
            max_area = max(min(height[right], height[left])*(right-left), max_area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area



# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
