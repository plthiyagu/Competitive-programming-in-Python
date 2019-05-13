'''
    Binary Search Tree type of data structure with logarithmic height (with high probability).
    Combines the BST and heap properties.

    Also support k-th element and median() operations.
'''


#########################################################################

import random

class TreapNode(object):
    def __init__(self, key):
        self.key = key
        self.ran = random.random()
        self.size = 1
        self.cnt = 1
        self.left = None
        self.right = None

    def left_rotate(self):
        a = self
        b = a.right
        a.right = b.left
        b.left = a
        a = b
        b = a.left
        b.size = b.left_size() + b.right_size() + b.cnt
        a.size = a.left_size() + a.right_size() + a.cnt
        return a

    def right_rotate(self):
        a = self
        b = a.left
        a.left = b.right
        b.right = a
        a = b
        b = a.right
        b.size = b.left_size() + b.right_size() + b.cnt
        a.size = a.left_size() + a.right_size() + a.cnt
        return a

    def left_size(self):
        return 0 if self.left is None else self.left.size

    def right_size(self):
        return 0 if self.right is None else self.right.size

class Treap(object):
    def __init__(self):
        self.root = None

    def _insert(self, node, key):
        if node is None:
            node = TreapNode(key)
            return node
        node.size += 1
        if key < node.key:
            node.left = self._insert(node.left, key)
            if node.left.ran < node.ran:
                node = node.right_rotate()
        elif key >= node.key:
            node.right = self._insert(node.right, key)
            if node.right.ran < node.ran:
                node = node.left_rotate()
        return node

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _find(self, node, key):
        if node == None:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def find(self, key):
        return self._find(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return False
        if node.key == key:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                if node.left.ran < node.right.ran:
                    node = node.right_rotate()
                    node.right = self._delete(node.right, key)
                else:
                    node = node.left_rotate()
                    node.left = self._delete(node.left, key)
        elif key < node.key:
            node.left = self._delete(node.left, key)
        else:
            node.right = self._delete(node.right, key)
        node.size = node.left_size() + node.right_size() + node.cnt
        return node

    def delete(self, key):
        if self.find(key) is None: return False
        self.root = self._delete(self.root, key)
        return True

    def _find_kth(self, node, k):
        if node is None: return None
        if k <= node.left_size():
            return self._find_kth(node.left, k)
        if k > node.left_size() + node.cnt:
            return self._find_kth(node.right, k - node.left_size() - node.cnt)
        return node

    def find_kth(self, k):
        if k <=0 or k > self.size():
            return None
        return self._find_kth(self.root, k)

    def size(self):
        return 0 if self.root is None else self.root.size

    def median(self):
        s = self.size()
        if s == 0: return 0
        result = 0
        if s % 2 == 1:
            result = self.find_kth(s // 2 + 1).key
        else:
            result = (self.find_kth(s // 2).key + self.find_kth(s // 2 + 1).key) / 2.0
        if result == int(result): result = int(result)
        return result

#########################################################################










'''    Verification test    '''
if __name__ == "__main__":
    from random import shuffle, randint
    from time import clock
    from heapq import nsmallest
    for l in range(1, 7):
        arr = list(range(1, 10**l))
        k = randint(1, len(arr))
        shuffle(arr)

        start = clock()
        T = Treap()
        for x in arr:
            T.insert(x)
        print('Treap building', clock() - start)
        start = clock()
        assert k == T.find_kth(k).key
        print('Treap find_kth for length 10 ^', l , '; k =', k, clock() - start)

        start = clock()
        n = nsmallest(k, arr)[k-1]
        assert n == k
        print('heapq for length 10 ^', l , ': k =', k,  clock() - start)
