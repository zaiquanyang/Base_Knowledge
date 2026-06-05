from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        curr = dummy
        carry = 0

        while l1 or l2 or carry:
            val = carry
            if l1:
                val += l1.val
                l1 = l1.next
            if l2:
                val += l2.val
                l2 = l2.next
            carry, val = divmod(val, 10)
            curr.next = ListNode(val)
            curr = curr.next

        return dummy.next


# 测试辅助函数
def make_list(nums):
    dummy = ListNode()
    curr = dummy
    for n in nums:
        curr.next = ListNode(n)
        curr = curr.next
    return dummy.next

def list_to_array(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


if __name__ == "__main__":
    sol = Solution()

    # 示例 1: 342 + 465 = 807 → [7,0,8]
    l1 = make_list([2, 4, 3])
    l2 = make_list([5, 6, 4])
    print(list_to_array(sol.addTwoNumbers(l1, l2)))  # [7, 0, 8]

    # 示例 2: 0 + 0 = 0 → [0]
    l1 = make_list([0])
    l2 = make_list([0])
    print(list_to_array(sol.addTwoNumbers(l1, l2)))  # [0]

    # 示例 3: 9999999 + 9999 = 10009998 → [8,9,9,9,0,0,0,1]
    l1 = make_list([9, 9, 9, 9, 9, 9, 9])
    l2 = make_list([9, 9, 9, 9])
    print(list_to_array(sol.addTwoNumbers(l1, l2)))  # [8, 9, 9, 9, 0, 0, 0, 1]
