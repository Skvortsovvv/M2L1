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

    def print(self):
        # используем обход в ширину
        queue_to_visit = queue.Queue()
        if self.root is None:
            print('_ _')
            return
        else:
            print('[' + str(self.root.key) + ' ' + self.root.value + ']')
        if self.root.left is not self.root.right:
            queue_to_visit.put(self.root.left)
            queue_to_visit.put(self.root.right)
            items_on_level = 2
            i = 0
            indexes = queue.Queue()
            index = -3
            flag = False
            while not queue_to_visit.empty():

                if i == index+index:  # or i == index+index+1
                    flag = True
                    sys.stdout.write('_ _')
                    indexes.put(i)
                    indexes.put(i+1)
                    index = indexes.get()
                    i += 2
                    if i is not items_on_level:
                        sys.stdout.write(' ')
                    else:
                        items_on_level *= 2
                        i = 0
                        sys.stdout.write('\n')
                        if (indexes.qsize() * 2 + queue_to_visit.qsize() + 2) <= items_on_level:
                            break
                    continue

                peak = queue_to_visit.get()
                if peak is None:
                    indexes.put(i)
                    sys.stdout.write('_')

                else:
                    sys.stdout.write('[' + str(peak.key) + ' ' + peak.value + ' ' + str(peak.parent.key) + ']')
                    queue_to_visit.put(peak.left)
                    queue_to_visit.put(peak.right)
                i += 1

                if i == items_on_level:
                    items_on_level *= 2
                    i = 0
                    sys.stdout.write('\n')
                    if not indexes.empty() and not flag:
                        index = indexes.get()
                    if (indexes.qsize()*2 + queue_to_visit.qsize()+2) < items_on_level:
                        break
                else:
                    sys.stdout.write(' ')

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
        right = self.find(right, left.key)
        right.left, left.parent = left, right
        return right

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

    if re.fullmatch(r"^add [\d+]+ [^\s+]+", text) is not None:
        pos1 = text[4:].find(' ')
        key = int(text[4:pos1+4])
        if key not in tree.Peaks:
            value = text[pos1+5:]
            tree.add_peak(Node(key, value))
            tree.root = tree.find(tree.root, key)
        else:
            tree.root = tree.find(tree.root, key)
        return

    if tree.root is not None:
        if re.fullmatch(r"set [\d+]+ [^\s+]+", text) is not None:
            pos1 = text[4:].find(' ')
            key = int(text[4:pos1+4])
            if key in tree.Peaks:
                value = text[pos1 + 5:]
                tree.root = tree.find(tree.root, key)
                tree.root.value = value
            else:
                tree.root = tree.find(tree.root, key)
            return

        if re.fullmatch(r'delete [\d+]+', text) is not None:
            key = int(text[7:])
            if key in tree.Peaks:
                tree.root = tree.find(tree.root, key)
                tree.root = tree.remove(tree.root, key)
            else:
                tree.root = tree.find(tree.root, key)
            return

        if re.fullmatch(r'search [\d+]+', text) is not None:
            key = int(text[7:])
            tree.root = tree.find(tree.root, key)
            if tree.root.key == key:
                print('1', tree.root.value)
            else:
                print('0')
            return

        if re.fullmatch(r'max', text) is not None:
            maximum = tree.max()
            tree.root = tree.find(tree.root, maximum)
            print(maximum)
            return

        if re.fullmatch(r'min', text) is not None:
            minimum = tree.min()
            tree.root = tree.find(tree.root, minimum)
            print(minimum)
            return

        if re.fullmatch(r'print', text) is not None:
            #print(tree.height(tree.root))
            tree.print()
            return

    print("error")



def main():

    tree = SplayTree()
    inputfile = open('MODUL2/tests2/input1.txt', 'r')


    # for text in inputfile:
    #     sys.stdout.write(text)
    #     process(text, tree)
    while True:
        try:
            text = input()
            process(text, tree)
        except EOFError:
            break
    return


main()
