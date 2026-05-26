# Verify if a Linked List is palindrome, with 1 recursive call and no pre-computations.
# Author: Giuseppe Tavella

# This is an input class. Do not edit.
class LinkedList:
    def __init__(self, value):
        self.value = value
        self.next = None

        
# O(n) time, where n is the number of nodes, 
#   because we have to traverse the entire linked list
# O(n) space, because we are there will be exactly n call frames
#   in the call stack, one for each linked list node
        
# TECHNIQUE: use recursion and mimic "going up" the linked list
#    as a natural side effect of a recursive call, specifically,
#    between the return of the recursive call and the return of the current
#    function. this is the place where we can simoultaneously
#    have information coming from the last node (so we know the nodes total)
#    as well as information frozen in that moment in time where
#    this function was called. so, in this space, we have 
#    access to both the nodes total as well as the index of that node.
#    it's like going to the future and then returning to the present
#    being able to compute new information based on information in that future (last node)

# TECHNIQUE: calculate how many nodes are in the tree, by getting
#    to the end of the linked list, and having that nodes total
#    be bubbled up as is with every return
# 
# TECHNIQUE: use a simple object (constant space) that keeps track of
#     the curr node of the "mirror 2" part of the linked list
#     with some thought, it may be possible to remove even that?

# ********* EXAMPLE (odd number of nodes)
# 
# RECURSIVE CALL 
# ------------------------------------------->
#                 ---- currNode = first node of mirror 1, seen from recursive call
#                 |             ----- currNode.next.next 
#                 |             |
#   0  ->  1  ->  2  ->  3  ->  2  ->  1  ->  0
# |                |           |               |
# ------------------           -----------------
#    MIRROR 1                      MIRROR 2     
#
# <--------------------------------------------
#  RECURSIVE CALL 

# ********** EXAMPLE (even number of nodes)
# 
# RECURSIVE CALL 
# ------------------------------------------->
#                 ---- currNode = first node of mirror 1, seen from recursive call
#                 |       ----- currNode.next
#                 |       |
#   0  ->  1  ->  2   ->  2  ->  1  ->  0
# |                |     |               |
# ------------------     -----------------
#    MIRROR 1                MIRROR 2     
#
# <--------------------------------------------
#  RECURSIVE CALL 

def linkedListPalindrome(head):
    info = {
        "startIdx": None,
        "currNodeMirror2": None
    }
    result = traverse(head, 0, info)
    return result["isPalindromeSoFar"]


def traverse(currNode, nodeIdx, info):
        
    if currNode is None:
        return {
            # +1 because this is how we calculate the length, when substract a start from an end
            # -1 because the current node is none, so we actually need to remove 1
            # therefore we do add +1-1 
            "nodesCount": nodeIdx,
            "isPalindromeSoFar": True,
        }
        
    result = traverse(currNode.next, nodeIdx+1, info)

    # is the number of nodes even?
    hasEvenNodes = result["nodesCount"] % 2 == 0
    # are we at the first mirror (or sub-linked list)
    # where we test palindromicity against the
    # other mirror of the linked list?
    areWeinMirror1 = nodeIdx < (result["nodesCount"] // 2)
    # this is the very first node from the right
    # seen from the point of view of the recursive call which is
    # returning from the previous call
    isLastNodeOfMirror1 = areWeinMirror1 and (nodeIdx == ((result["nodesCount"] // 2) - 1))

    # print(nodeIdx, currNode.value, result, f"areWeinMirror1: {areWeinMirror1}")
    
    isPalindromeValue = True
    
    # if we are not in mirror1, we don't care
    if areWeinMirror1:
        # even number of nodes
        if hasEvenNodes:
            info["currNodeMirror2"] = currNode.next if isLastNodeOfMirror1 else info["currNodeMirror2"].next
        # odd number of nodes
        else:
            # currNode.next.next because we skip the node in the "middle"
            info["currNodeMirror2"] = currNode.next.next if isLastNodeOfMirror1 else info["currNodeMirror2"].next
            
        isPalindromeValue = currNode.value == info["currNodeMirror2"].value
    
    return {
        # nodes count remains the same, we simply 
        # pass it from node to node
        "nodesCount": result["nodesCount"],
        # if there is only one false value, the and will guaranteed
        # to bring that value to the first call
        "isPalindromeSoFar": result["isPalindromeSoFar"] and isPalindromeValue
    }





