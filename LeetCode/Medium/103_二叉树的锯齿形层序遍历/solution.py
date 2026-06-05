from typing import List, Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # 注意使用 deque 构造双向队列
        if not root:
            return []

        queue = deque()
        queue.append(root)

        ans = []
        left_2_right = True
        while queue:
            level_size = len(queue)
            level_ans = []

            for i in range(level_size):
                tmp_node = queue.popleft()
                level_ans.append(tmp_node.val)

                if tmp_node.left:
                    queue.append(tmp_node.left)
                if tmp_node.right:
                    queue.append(tmp_node.right)
            
            if not left_2_right:
                level_ans.reverse()
                
            ans.append(level_ans)

            left_2_right = not left_2_right
        
        return ans

# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
