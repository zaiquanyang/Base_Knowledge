from typing import List, Optional

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # 回溯实现，每一次只有两种选择，要么把当前遇到的数字加入path，要么不加入
        ans = []
        def backback(num_idx, path):
            # 先记录答案
            ans.append(path[:]) # path[:] 是浅拷贝

            for i in range(num_idx, len(nums)):
                # 选择加入
                path.append(nums[i])
                backback(i+1, path)

                # 选择不加入
                path.pop()
                
        backback(0, [])

        return ans


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
