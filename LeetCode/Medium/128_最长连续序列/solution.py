from typing import List, Optional


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums_set = set(nums)

        max_seq_len = 0
        for num in nums_set:
            if (num-1) not in nums_set:
                current_num = num
                sequence_len = 1

                while current_num+1 in nums_set:
                    current_num += 1
                    sequence_len += 1

                max_seq_len = max(max_seq_len, sequence_len)
        return max_seq_len

# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
