import sys
import re
import math

class Heap:

    def __init__(self):
        self.peaks = []  # list из [ключ, значение]
        self.keys = {}  # map из ключей и индексов

    def heapify(self, index):
        left = 2*index + 1
        right = 2*index + 2
        minimum = index
        if (left < len(self.peaks)) and (self.peaks[left][0] < self.peaks[minimum][0]):
            minimum = left
        if (right < len(self.peaks)) and (self.peaks[right][0] < self.peaks[minimum][0]):
            minimum = right
        if minimum is not index:

            self.swap_peaks(index, minimum)
            self.swap_indexes(self.peaks[index][0], self.peaks[minimum][0])

            self.heapify(minimum)

    def make_heap(self):
        for i in range(int(len(self.peaks)/2)-1, -1):
            self.heapify(i)

    def find(self, key):

        index = None
        try:
            index = self.keys[key]
        except KeyError:
            pass
        return index

    def set(self, key, value):
        index = self.keys.get(key)
        self.peaks[index][1] = value

    def parent_index(self, child_index):
        if child_index == 0:
            return None
        if child_index % 2 == 0:
            # левый
            return (child_index - 2) // 2
        else:
            # правый
            return (child_index - 1) // 2

    def add(self, key, value):
        self.peaks.append([key, value])
        i = len(self.peaks) - 1
        self.keys[key] = i
        while (i > 0) and (self.peaks[self.parent_index(i)][0] > key):
            p = self.parent_index(i)

            self.swap_peaks(p, i)
            self.swap_indexes(self.peaks[p][0], self.peaks[i][0])

            i = self.parent_index(i)

    def min(self):
        return self.peaks[0]

    def max(self):
        index_max = 0
        length1 = length2 = len(self.peaks)
        a = 0
        while length1 > 1:
            length1 = int(length1 / 2)
            a += 1
        power = pow(2, a) - 1
        amount1 = length2 - power  # число листов на последнем уровне
        b = math.ceil(amount1/2)  # число предков листов последнего уровня
        amount2 = pow(2, a-1) - b  # число листов на предпоследнем уровне
        for i in range(length2 - amount1 - amount2, length2):
            if self.peaks[i][0] > self.peaks[index_max][0]:
                index_max = i
        return self.peaks[index_max]

    def extract(self):
        top = self.peaks[0]
        index = len(self.peaks)-1
        key = self.peaks[0][0]
        self.peaks[0] = self.peaks[index]
        del self.peaks[index:index+1]
        del self.keys[key]
        self.heapify(0)
        return top

    def swap_peaks(self, child, parent):
        self.peaks[parent], self.peaks[child] = self.peaks[child], self.peaks[parent]

    def swap_indexes(self, key1, key2):
        self.keys[key1], self.keys[key2] = self.keys[key2], self.keys[key1]

    def delete(self, key):
        last = len(self.peaks) - 1
        if key == self.peaks[last][0]:
            del self.peaks[last:last+1]
            del self.keys[key]
        else:
            index = self.keys[key]

            self.swap_peaks(index, last)
            self.swap_indexes(self.peaks[index][0], self.peaks[last][0])

            del self.peaks[last:last+1]
            del self.keys[key]

            key_last = self.peaks[index][0]  # ключ перемещаемого вверх элемента

            if index == 0 or self.peaks[self.parent_index(index)][0] < self.peaks[index][0]:
                self.heapify(index)
            else:
                while self.parent_index(index) is not None:
                    if self.peaks[self.parent_index(index)][0] > self.peaks[index][0]:
                        parent = self.parent_index(index)  # индекс родителя

                        self.swap_peaks(index, parent)
                        parent = index  # обновляем индекс родителя
                        self.swap_indexes(key_last, self.peaks[parent][0])

                        index = self.keys[key_last]  # обновляем индекс перемещенного вверх элеента
                        self.heapify(parent)  # возобновляем св-во кучи относительно перемещенного родителя
                    else:
                        break

    def print(self, out=sys.stdout):

        if len(self.peaks) == 0:
            print('_', file=out)
            return
        counter = 2
        counter_lvl = 1
        for i in range(0, len(self.peaks)):
            if i == 0:
                print('[' + str(self.peaks[i][0]) + ' ' + self.peaks[i][1] + ']', file=out)
            else:
                if i % 2 != 0:
                    out.write('[' + str(self.peaks[i][0]) + ' '
                                     + self.peaks[i][1] + ' ' + str(self.peaks[(i-1)//2][0]) + ']')
                else:
                    out.write('[' + str(self.peaks[i][0]) + ' '
                                     + self.peaks[i][1] + ' ' + str(self.peaks[(i-2)//2][0]) + ']')
                if counter_lvl != counter:
                    out.write(' ')
                    counter_lvl += 1
                else:
                    out.write('\n')
                    counter_lvl = 1
                    counter *= 2

        a = 1  # степень двойки
        size1 = size2 = len(self.peaks)
        while size1 > 1:
            size1 = int(size1 / 2)
            a += 1
        power = pow(2, a) - 1
        if power != size2:
            amount = power - size2
            out.write('_ ' * (amount - 1))
            out.write('_\n')


def process(heap: Heap, command):
    if command == ' ':
        return
    if re.fullmatch(r'add [-]?[\d+]+ [^\s+]+', command) is not None:
        pos1 = command[4:].find(' ')
        key = int(command[4:pos1 + 4])
        index = heap.find(key)
        if index is None:
            value = command[pos1+5:]
            heap.add(key, value)
        else:
            print('error')
        return
    if re.fullmatch(r"set [-]?[\d+]+ [^\s+]+", command) is not None:
        pos1 = command[4:].find(' ')
        key = int(command[4:pos1 + 4])
        index = heap.find(key)
        if index is not None:
            value = command[pos1 + 5:]
            heap.set(key, value)
        else:
            print('error')
        return
    if re.fullmatch(r'delete [-]?[\d+]+', command) is not None:
        if len(heap.keys) != 0:
            key = int(command[7:])
            if heap.find(key) is not None:
                heap.delete(key)
            else:
                print('error')
        else:
            print('error')
        return
    if re.fullmatch(r'search [-]?[\d+]+', command) is not None:
        key = int(command[7:])
        index = heap.find(key)
        if index is not None:
            print(1, index, heap.peaks[index][1])
        else:
            print(0)
        return
    if re.fullmatch(r'min', command) is not None:
        if len(heap.keys) != 0:
            minimum = heap.min()
            print(minimum[0], 0, minimum[1])
        else:
            print('error')
        return
    if re.fullmatch(r'max', command) is not None:
        if len(heap.keys) != 0:
            maximum = heap.max()
            print(maximum[0], heap.keys[maximum[0]], maximum[1])
        else:
            print('error')
        return
    if re.fullmatch(r'extract', command) is not None:
        if len(heap.keys) != 0:
            top = heap.extract()
            print(top[0], top[1])
        else:
            print('error')
        return
    if re.fullmatch(r'print', command) is not None:
        heap.print()
        return


if __name__ == '__main__':
    min_heap = Heap()

    while True:
        try:
            text = input()
            process(min_heap, text)
        except EOFError:
            break

