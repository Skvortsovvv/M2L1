import re
import queue
import sys


class Node:

    def __init__(self, key=None, value=None, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent


class SplayTree:

    root = None
    Peaks = []
    h = 0

    def __init__(self):
        self.root = None

    def add_peak(self, peak: Node):
        if self.root is None:
            self.root = peak
            self.Peaks.append(peak.key)
            return
        x = self.root
        while x is not None:
            if x.key < peak.key:
                if x.right is None:
                    x.right = peak
                    x.right.parent = x
                    break
                else:
                    x = x.right
            elif x.key > peak.key:
                if x.left is None:
                    x.left = peak
                    x.left.parent = x
                    break
                else:
                    x = x.left
        self.Peaks.append(peak.key)


    def set_parent(self, child: Node, parent):
        if child is not None:
            if child.value is not None:
                child.parent = parent

    def keep_parent(self, child):
        self.set_parent(child.left, child)
        self.set_parent(child.right, child)

    def max(self):
        x = self.root
        while x.right is not None:
            x = x.right
        return x.key

    def min(self):
        x = self.root
        while x.left is not None:
            x = x.left
        return x.key

    def print(self, out=sys.stdout):

        queue_to_visit = queue.Queue()  # items
        if self.root is None:
            out.write('_\n')
            return
        else:
            out.write('[' + str(self.root.key) + ' ' + self.root.value + ']\n')
        if self.root.left is not self.root.right:
            queue_to_visit.put(self.root.left)
            queue_to_visit.put(self.root.right)

        items_on_level = 2
        i = 0
        indexes_of_items = queue.Queue()  # items`s indexes
        index = -1
        high = 1
        size_before = 0
        while not queue_to_visit.empty():

            if size_before > 0:
                index = indexes_of_items.get()
                size_before -= 1

            if index > i:
                out.write('_ ' * (index - i - 1))
                i = index

                if (size_before == 0) and (index < items_on_level - 1) and (index != -1):
                    out.write(' ')
                    out.write('_ ' * (items_on_level - index - 2))
                    out.write('_')
                    i = items_on_level

                if i == items_on_level:
                    out.write('_')
                    items_on_level *= 2
                    i = 0

                    out.write('\n')
                    high += 1
                    size_before = indexes_of_items.qsize()
                    if high == self.h:
                        break
                else:
                    out.write('_ ')

            peak = queue_to_visit.get()
            if peak is None:
                out.write('_')

            else:
                out.write('[' + str(peak.key) + ' ' + peak.value + ' ' + str(peak.parent.key) + ']')
                queue_to_visit.put(peak.left)
                queue_to_visit.put(peak.right)
                indexes_of_items.put(i + i)
                indexes_of_items.put(i + i + 1)
            i += 1

            if (size_before == 0) and (index < items_on_level - 1) and (index != -1):
                out.write(' ')
                out.write('_ ' * (items_on_level - index - 2))
                out.write('_')
                i = items_on_level

            if i == items_on_level:
                items_on_level *= 2
                i = 0
                out.write('\n')
                high += 1
                if high == self.h:
                    break
                size_before = indexes_of_items.qsize()
            else:
                out.write(' ')

    def rotate(self, parent, child):
        gparent = parent.parent
        if gparent is not None:
            if gparent.left == parent:
                gparent.left = child
            else:
                gparent.right = child

        if parent.left == child:
            parent.left, child.right = child.right, parent
        else:
            parent.right, child.left = child.left, parent

        self.keep_parent(child)
        self.keep_parent(parent)
        child.parent = gparent


    def splay(self, v: Node):
        if v.parent is None:
            return v
        parent = v.parent
        gparent = parent.parent
        if gparent is None:
            self.rotate(parent, v)
            return v
        else:
            zigzig = (gparent.left == parent) == (parent.left == v)
            if zigzig:
                self.rotate(gparent, parent)
                self.rotate(parent, v)
            else:
                self.rotate(parent, v)
                self.rotate(gparent, v)
            return self.splay(v)


    def find(self, v, key): # v - root
        if v is None:
            return None
        if key == v.key:
            return self.splay(v)
        if key < v.key and v.left is not None:
            return self.find(v.left, key)
        if key > v.key and v.right is not None:
            return self.find(v.right, key)
        return self.splay(v)


    def merge(self, left, right):
        if right == None:
            return left
        if left == None:
            return right
        left = self.find(left, right.key)
        left.right, right.parent = right, left
        return left


    def remove(self, root, key):
        self.set_parent(root.left, None)
        self.set_parent(root.right, None)
        return self.merge(root.left, root.right)

    def height(self, root: Node):
        if root is None:
            return 0
        else:
            return 1+max(self.height(root.left), self.height(root.right))


def process(text, tree: SplayTree):
    if len(text) == 0:
        return

    if re.fullmatch(r"^add [-]?[\d+]+ [^\s+]+", text) is not None:
        pos1 = text[4:].find(' ')
        key = int(text[4:pos1+4])
        if key not in tree.Peaks:
            value = text[pos1+5:]
            tree.add_peak(Node(key, value))
            tree.root = tree.find(tree.root, key)
        else:
            tree.root = tree.find(tree.root, key)
            print('error')
        return

    if re.fullmatch(r"set [-]?[\d+]+ [^\s+]+", text) is not None:
        pos1 = text[4:].find(' ')
        key = int(text[4:pos1+4])
        tree.root = tree.find(tree.root, key)
        if key in tree.Peaks:
            value = text[pos1 + 5:]
            tree.root.value = value
        else:
            print('error')
        return

    if re.fullmatch(r'delete [-]?[\d+]+', text) is not None:
        key = int(text[7:])
        tree.root = tree.find(tree.root, key)
        if key in tree.Peaks:
            tree.root = tree.remove(tree.root, key)
            tree.Peaks.remove(key)
        else:
            print('error')
        return

    if re.fullmatch(r'search [-]?[\d+]+', text) is not None:
        key = int(text[7:])
        tree.root = tree.find(tree.root, key)
        if key in tree.Peaks:
            print('1', tree.root.value)
        else:
            print('0')
        return

    if re.fullmatch(r'max', text) is not None:
        if len(tree.Peaks) != 0:
            maximum = tree.max()
            tree.root = tree.find(tree.root, maximum)
            print(maximum, tree.root.value)
        else:
            print('error')
        return

    if re.fullmatch(r'min', text) is not None:
        if len(tree.Peaks) != 0:
            minimum = tree.min()
            tree.root = tree.find(tree.root, minimum)
            print(minimum, tree.root.value)
        else:
            print('error')
        return

    if re.fullmatch(r'print', text) is not None:
        if len(tree.Peaks) == 0:
            print('_')
            return
        tree.h = tree.height(tree.root)
        tree.print()
        return

    print("error")



def main():

    sys.setrecursionlimit(10000)

    tree = SplayTree()

    while True:
        try:
            text = input()
            process(text, tree)
        except EOFError:
            break

    return


main()
