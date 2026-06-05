from typing import List, Optional


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        
        left_bound, right_bound, upper_bound, bottom_bound = 0, len(matrix[0])-1, 0, len(matrix)-1
        ans = []
        m, n = 0, 0
        ans.append(matrix[m][n])
        while upper_bound<=bottom_bound and left_bound<=right_bound:
            # 往右走 
            while n < right_bound:
                n += 1
                ans.append(matrix[m][n])
            upper_bound += 1
            if upper_bound > bottom_bound:
                break
            # print("往右走", ans) # 
            # print(left_bound, right_bound, upper_bound, bottom_bound)
            # 往下走
            while m<bottom_bound:
                m += 1
                ans.append(matrix[m][n])
            right_bound -= 1
            if left_bound > right_bound:
                break
            # print("往下走", ans)
            # print(left_bound, right_bound, upper_bound, bottom_bound)
            # 往左走
            while n > left_bound:
                n -= 1
                ans.append(matrix[m][n])
            bottom_bound -= 1
            if upper_bound>bottom_bound:
                break
            # print("往左走", ans)
            # print(left_bound, right_bound, upper_bound, bottom_bound)
            # 往上走
            while m > upper_bound:
                m -= 1
                ans.append(matrix[m][n])
            left_bound += 1
            # print("往上走", ans)
            # print(left_bound, right_bound, upper_bound, bottom_bound)
            if left_bound>right_bound:
                break
        return ans


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
