from typing import List, Optional


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        ans_dict_row = {}
        ans_dict_col = {}
        ans_dict_block = {}

        for i in range(9):
            ans_dict_row[i] = []
            ans_dict_col[i] = []
            ans_dict_block[i] = []

        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    continue

                k = i//3*3 + j//3
                key = str(i) + str(j) + str(k)
                
                if (board[i][j] in ans_dict_row[i]) or (board[i][j] in ans_dict_col[j]) or (board[i][j] in ans_dict_block[k]):
                    return False
                else:
                    ans_dict_row[i].append(board[i][j])
                    ans_dict_col[j].append(board[i][j])
                    ans_dict_block[k].append(board[i][j])

                
        return True



# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
