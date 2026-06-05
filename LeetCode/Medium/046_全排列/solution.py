from typing import List, Optional


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        ans_list = []
        N = len(nums)

        def back_track(ans, nums):
            if len(ans) == N:
                ans_list.append(ans.copy())
                return 
            n = len(nums)

            for i in range(n):
                ans.append(nums[i])
                tmp_nums = nums[:i] + nums[i+1:]
                back_track(ans, tmp_nums)

                ans.pop()

        back_track([], nums)
        return ans_list


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
