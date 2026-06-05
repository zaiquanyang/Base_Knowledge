from typing import List, Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # 注意使用 deque这个对象

        node_queue = deque()
        node_queue.append(root)
        ans = []

        if not root:
            return []

        while node_queue:
            level_size = len(node_queue)
            level_ans = []
            for i in range(level_size):
                node_tmp = node_queue.popleft()
                
                level_ans.append(node_tmp.val)

                if node_tmp.left:
                    node_queue.append(node_tmp.left)
                if node_tmp.right:
                    node_queue.append(node_tmp.right)
            
            ans.append(level_ans)
        return ans

# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
