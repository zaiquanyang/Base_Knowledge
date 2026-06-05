from typing import List, Optional


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        in_order_map = {val: i for i, val in enumerate(inorder)}

        self.pre_idx = 0
        def build_helper(left, right):
            if left>right:
                return None
            
            root_val = preorder[self.pre_idx]
            root_idx = in_order_map[root_val]
            root_node = TreeNode(root_val)
            self.pre_idx += 1

            root_node.left = build_helper(left, root_idx-1)
            root_node.right = build_helper(root_idx+1, right)

            
            return root_node
        
        return build_helper(0, len(preorder)-1)
            

# 测试
if __name__ == "__main__":
    sol = Solution()
    # TODO: 添加测试用例
    pass
