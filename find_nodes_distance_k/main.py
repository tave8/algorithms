# Find nodes with distance k, traversing the tree only once (no re-traversing already traversed nodes).
# Author: Giuseppe Tavella
        

# This is an input class. Do not edit.
class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# VARIANT WITH ALGORITHM THAT FINDS PATH OF A NODE
# this algorithm does traverse the tree only as necessary.
# to find the target node first, and then to find the nodes
# that are distant k from it
def findNodesDistanceK(tree, target, k):
    targetValue = target
    targetDistance = k
    # the list of values to return
    values = []
    # the ancestors of the target node
    # from left to right: root --> ... ---> grandparent --> direct parent
    ancestors = []
    
    (targetNode) = findNodeByValue(targetValue, tree, ancestors)
    
    # print(f"target node: {targetNode.value}")
    # for ancestor in ancestors:
    #     print(f"ancestor: {ancestor.value}")

    # find the values at the target distance.
    # you can do this now or later, it shouldn't matter
    findDescendantsAtDistance(targetDistance, targetNode, values, nodeToExclude=None)

    # the first lower parent in the tree is the target node that was found
    # that means, this node will be the first to be excluded
    # why? because its descendants that are k distant from it, have just been added
    # to the list of values
    lowerAncestor = targetNode
    # because in the loop we'll be working with parent nodes,
    # the initial value of new target distance is reduced by 1
    newTargetDistance = targetDistance-1
    # start from the direct parent of the target node,
    # so from the last ancestor in the list
    i = len(ancestors)-1

    # going back in the list of ancestors, means
    # navigating the tree from node to parent,
    # from parent to grandparent, and so on
    while newTargetDistance >= 0 and i >= 0:
        upperAncestor = ancestors[i]
        # this call will fill the values list,
        # with the values that have the given distance,
        # from the ancestor, excluding the node
        # right below the given node
        findDescendantsAtDistance(
            newTargetDistance, 
            upperAncestor, 
            values, 
            nodeToExclude=lowerAncestor
        )
        # the next target node is the parent node of the current node
        lowerAncestor = upperAncestor
        newTargetDistance -= 1
        i -= 1
    
    return values


# given a node, find the values of the nodes that have the 
# are descendants of the given node, and have the given target distance
def findDescendantsAtDistance(targetDistance, currTree, values, currDistance=0, nodeToExclude=None):
    # if current tree is none, or if current tree is a node
    # to exclude, skip it
    if currTree is None or currTree == nodeToExclude:
        return 
    if currDistance == targetDistance:
        values.append(currTree.value)
        return
    # at every level down the tree, the distance is increased by 1
    findDescendantsAtDistance(targetDistance, currTree.left, values, currDistance+1, nodeToExclude)
    findDescendantsAtDistance(targetDistance, currTree.right, values, currDistance+1, nodeToExclude)

    

# ALGORITHM: FIND PATH OF A NODE
# gives you the ancestors of a node
# in this case, we use it to find the ancestors of a node
# with a target value
def findNodeByValue(targetValue, currTree, ancestors):
    # target node not found. return none and ancestors
    if currTree is None:
        return (None)
        
    # target node found. return that node and ancestors
    if currTree.value == targetValue:
        return (currTree)
    
    # at ancestors[-1] i find the parent 
    # if len(ancestors) > 0:
    #     pass
    # of the current tree, if the current tree is not root
    # the return values are what 

    # as soon as you add the current tree as an ancestor, it means
    # that the current tree in the NEXT recursive call, will have 
    # its direct parent be the current tree in this time
    # therefore, there cannot be any code or functionality between
    # appending the current as the ancestor, and the recursive calls.
    # if you were to add code in between, 
    # ************************
    ancestors.append(currTree)
    # cannot add code here. as soon as you add the current tree as an ancestor
    # the last parent (current tree) will have just changed, so getting
    # ancestors[-1], which is supposed to get the parent of the current tree,
    # will give you the current tree itself, instead.
    (maybeTargetNode1) = findNodeByValue(targetValue, currTree.left, ancestors)
    (maybeTargetNode2) = findNodeByValue(targetValue, currTree.right, ancestors)
    # ************************
    
    # remove the ancestor, only if the target node was not found
    # why? if you don't do this check, you will remove every ancestor.
    # instead you must remove the ancestor, only if the previous calls have not
    # found the target node
    if not maybeTargetNode1 and not maybeTargetNode2:
        # because we're adding the current tree as the ancestor of the next
        # recursive call, we must immediately call the functions recursively
        ancestors.pop()

    # bubbles the currTree found back up to the first call
    return (
        # example: None or None or None or targetNode
        # will always return that targetNode
        maybeTargetNode1 or maybeTargetNode2
    )

    

