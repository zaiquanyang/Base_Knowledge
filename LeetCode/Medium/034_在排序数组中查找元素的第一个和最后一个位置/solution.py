from typing import List, Optional


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        N = len(nums)

        left, right = 0, N-1
        while left<=right:
            mid = (left+right)//2
            if nums[mid] == target:
                target_left, target_right = mid, mid
                
                while left<=(target_left-1):
                    if nums[target_left-1] == target:
                        target_left -= 1
                    else:
                        break
                
                while target_right+1<=right:
                    if nums[target_right+1] == target:
                        target_right += 1
                    else:
                        break

                return target_left, target_right

            if nums[mid]<target<=nums[right]:
                left = mid+1
            else:
                right=mid-1
        return [-1, -1]




# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
