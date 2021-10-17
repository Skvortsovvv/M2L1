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

    def print(self, fout):

        queue_to_visit = queue.Queue()  # items
        if self.root is None:
            fout.write('_\n')
            print('_')
            return
        else:
            fout.write('[' + str(self.root.key) + ' ' + self.root.value + ']\n')
            print('[' + str(self.root.key) + ' ' + self.root.value + ']')
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
                sys.stdout.write('_ ' * (index - i - 1))
                fout.write('_ ' * (index - i - 1))
                i = index

                if (size_before == 0) and (index < items_on_level - 1) and (index is not -1):
                    sys.stdout.write(' ')
                    fout.write(' ')
                    sys.stdout.write('_ ' * (items_on_level - index - 2))
                    fout.write('_ ' * (items_on_level - index - 2))
                    sys.stdout.write('_')
                    fout.write('_')
                    i = items_on_level

                if i == items_on_level:
                    sys.stdout.write('_')
                    fout.write('_')
                    items_on_level *= 2
                    i = 0

                    fout.write('\n')
                    sys.stdout.write('\n')
                    high += 1
                    size_before = indexes_of_items.qsize()
                    if high == self.h:
                        break
                else:
                    sys.stdout.write('_ ')
                    fout.write('_ ')

            peak = queue_to_visit.get()
            if peak is None:
                fout.write('_')
                sys.stdout.write('_')

            else:
                fout.write('[' + str(peak.key) + ' ' + peak.value + ' ' + str(peak.parent.key) + ']')
                sys.stdout.write('[' + str(peak.key) + ' ' + peak.value + ' ' + str(peak.parent.key) + ']')
                queue_to_visit.put(peak.left)
                queue_to_visit.put(peak.right)
                indexes_of_items.put(i + i)
                indexes_of_items.put(i + i + 1)
            i += 1

            if (size_before == 0) and (index < items_on_level - 1) and (index is not -1):
                sys.stdout.write(' ')
                fout.write(' ')
                sys.stdout.write('_ ' * (items_on_level - index - 2))
                fout.write('_ ' * (items_on_level - index - 2))
                sys.stdout.write('_')
                fout.write('_')
                i = items_on_level

            if i == items_on_level:
                items_on_level *= 2
                i = 0
                fout.write('\n')
                sys.stdout.write('\n')
                high += 1
                if high == self.h:
                    break
                size_before = indexes_of_items.qsize()
            else:
                fout.write(' ')
                sys.stdout.write(' ')

        # queue_to_visit = queue.Queue()
        # if self.root is None:
        #     fout.write('_\n')
        #     print('_')
        #     return
        # else:
        #     fout.write('[' + str(self.root.key) + ' ' + self.root.value + ']\n')
        #     print('[' + str(self.root.key) + ' ' + self.root.value + ']')
        # if self.root.left is not self.root.right:
        #     queue_to_visit.put(self.root.left)
        #     queue_to_visit.put(self.root.right)
        #     items_on_level = 2
        #     i = 0
        #     indexes = queue.Queue()
        #     index = -3
        #     flag = False
        #     high = 1
        #     while not queue_to_visit.empty():
        #         if i == index+index:  # or i == index+index+1
        #             flag = True
        #             fout.write('_ _')
        #             sys.stdout.write('_ _')
        #             indexes.put(i)
        #             indexes.put(i+1)
        #             index = indexes.get()
        #             i += 2
        #             if i is not items_on_level:
        #                 fout.write(' ')
        #                 sys.stdout.write(' ')
        #             else:
        #                 items_on_level *= 2
        #                 i = 0
        #                 fout.write('\n')
        #                 sys.stdout.write('\n')
        #                 high += 1
        #                 if high == self.h:
        #                     break
        #             continue
        #
                # peak = queue_to_visit.get()
                # if peak is None:
                #     indexes.put(i)
                #     fout.write('_')
                #     sys.stdout.write('_')
                #
                # else:
                #     fout.write('[' + str(peak.key) + ' ' + peak.value + ' ' + str(peak.parent.key) + ']')
                #     sys.stdout.write('[' + str(peak.key) + ' ' + peak.value + ' ' + str(peak.parent.key) + ']')
                #     queue_to_visit.put(peak.left)
                #     queue_to_visit.put(peak.right)
                # i += 1
                #
                # if i == items_on_level:
                #     items_on_level *= 2
                #     i = 0
                #     fout.write('\n')
                #     sys.stdout.write('\n')
                #     high += 1
                #     if high == self.h:
                #         break
                #     if not indexes.empty() and not flag:
                #         index = indexes.get()
                # else:
                #     fout.write(' ')
                #     sys.stdout.write(' ')

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


def process(text, tree: SplayTree, fout):
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
            fout.write('error\n')
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
            fout.write('error\n')
            print('error')
        return

    if re.fullmatch(r'delete [-]?[\d+]+', text) is not None:
        key = int(text[7:])
        tree.root = tree.find(tree.root, key)
        if key in tree.Peaks:
            tree.root = tree.remove(tree.root, key)
            tree.Peaks.remove(key)
        else:
            fout.write('error\n')
            print('error')
        return

    if re.fullmatch(r'search [-]?[\d+]+', text) is not None:
        key = int(text[7:])
        tree.root = tree.find(tree.root, key)
        if key in tree.Peaks:
            fout.write('1 ' + tree.root.value + '\n')
            print('1', tree.root.value)
        else:
            fout.write('0\n')
            print('0')
        return

    if re.fullmatch(r'max', text) is not None:
        if len(tree.Peaks) is not 0:
            maximum = tree.max()
            tree.root = tree.find(tree.root, maximum)
            fout.write(str(maximum) + ' ' + tree.root.value + '\n')
            print(maximum, tree.root.value)
        else:
            fout.write('error\n')
            print('error')
        return

    if re.fullmatch(r'min', text) is not None:
        if len(tree.Peaks) is not 0:
            minimum = tree.min()
            tree.root = tree.find(tree.root, minimum)
            fout.write(str(minimum) + ' ' + tree.root.value+ '\n')
            print(minimum, tree.root.value)
        else:
            fout.write('error\n')
            print('error')
        return

    if re.fullmatch(r'print', text) is not None:
        if len(tree.Peaks) == 0:
            fout.write('_\n')
            print('_')
            return
        tree.h = tree.height(tree.root)
        tree.print(fout)
        return

    print("error")



def main():

    sys.setrecursionlimit(10000)

    tree = SplayTree()
    fin = open('MODUL2/tests2/input15.txt', "r")
    fout = open('check.txt', 'w')
    for text in fin:
        t = text
        process(text.strip(), tree, fout)
    fin.close()

    # while True:
    #     try:
    #         text = input()
    #         process(text, tree, fout)
    #     except EOFError:
    #         break
    return


main()
