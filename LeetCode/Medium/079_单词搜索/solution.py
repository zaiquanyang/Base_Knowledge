from typing import List, Optional


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        
        m, n = len(board), len(board[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        def back_track(s, k, path_len):
            # 如果找到符合 word 内容的路径，返回 True
            if path_len == len(word):
                return True
            # 把已经添加到 path 的board[s][k]暂时置为 #， 避免
            tmp = board[s][k]
            board[s][k] = '#'

            for sk in directions:
                s_, k_ = s+sk[0], k+sk[1]
                if 0<=s_<m and 0<=k_<n and board[s_][k_] == word[path_len]:
                    if back_track(s_, k_, path_len+1):
                        return True
            # 四个方向的遍历结果都没合适的
            board[s][k] = tmp

            return False

        # 遍历整个 board, 查找第一个开头字符匹配字符串的位置开始回溯
        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0]:
                    if back_track(i, j, 1):
                        return True
        
        return False



        

# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
