from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        N = len(nums)
        left, right = 0, N-1

        while left <= right:
            # print(left, right)
            mid = (left + right)//2
            if nums[mid]==target:
                return mid

            # left--->mid 是左半递增区间
            if nums[left] <= nums[mid]:
                if nums[left]<=target<nums[mid]:
                    right=mid-1
                else:
                    left = mid+1
            else: # mid--->right 是递增区间
                if nums[mid]<target<=nums[right]:
                    left = mid+1
                else:
                    right=mid-1
        return -1
