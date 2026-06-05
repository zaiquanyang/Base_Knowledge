from typing import List, Optional


class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return "1"
        
        # 计算 n-1
        pre_str_list=self.countAndSay(n-1)

        cur_str_list = []
        cur_str = ""
        cur_num = 0
        for i in range(len(pre_str_list)):
            if pre_str_list[i] != cur_str:
                if cur_str != "":
                    cur_str_list.append(str(cur_num))
                    cur_str_list.append(cur_str)
                cur_str = pre_str_list[i]
                cur_num = 1
            else:
                cur_num += 1
        
        cur_str_list.append(str(cur_num))
        cur_str_list.append(cur_str)
        # print(n, "".join(cur_str_list))
        return "".join(cur_str_list)


# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
