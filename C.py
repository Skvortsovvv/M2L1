import sys
import re
import time

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
            self.peaks[index], self.peaks[minimum] = self.peaks[minimum], self.peaks[index]
            self.keys[self.peaks[index][0]], self.keys[self.peaks[minimum][0]] \
                = self.keys[self.peaks[minimum][0]], self.keys[self.peaks[index][0]]
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
        # for i in range(0, len(self.peaks)):
        #     if self.peaks[i][0] == key:
        #         return i
        # return None

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
            self.peaks[p], self.peaks[i] = self.peaks[i], self.peaks[p]
            self.keys[self.peaks[p][0]], self.keys[self.peaks[i][0]] \
                = self.keys[self.peaks[i][0]], self.keys[self.peaks[p][0]]
            i = self.parent_index(i)

    def min(self):
        print(self.peaks[0][0], 0, self.peaks[0][1])

    def max(self):
        index_max = 0
        for i in range(0, len(self.peaks)):
            if self.peaks[i][0] > self.peaks[index_max][0]:
                index_max = i
        print(self.peaks[index_max][0], index_max, self.peaks[index_max][1])

    def extract(self):
        index = len(self.peaks)-1
        key = self.peaks[0][0]
        print(self.peaks[0][0], self.peaks[0][1])
        self.peaks[0] = self.peaks[index]
        del self.peaks[index:index+1]
        del self.keys[key]
        self.heapify(0)

    def delete(self, key):
        last = len(self.peaks) - 1
        if key == self.peaks[last][0]:
            del self.peaks[last:last+1]
            del self.keys[key]
        else:
            index = self.keys[key]
            self.peaks[index], self.peaks[last] = self.peaks[last], self.peaks[index]
            self.keys[self.peaks[index][0]], self.keys[self.peaks[last][0]] \
                = self.keys[self.peaks[last][0]], self.keys[self.peaks[index][0]]
            del self.peaks[last:last+1]
            del self.keys[key]

            key_last = self.peaks[index][0]  # ключ перемещаемого вверх элемента

            if index == 0 or self.peaks[self.parent_index(index)][0] < self.peaks[index][0]:
                self.heapify(index)
            else:
                while self.parent_index(index) is not None:
                    if self.peaks[self.parent_index(index)][0] > self.peaks[index][0]:
                        parent = self.parent_index(index)  # индекс родителя
                        self.peaks[parent], self.peaks[index] = \
                            self.peaks[index], self.peaks[parent]  # меняем местами родителя и перемещаемый эелемент
                        parent = index  # обновляем индекс родителя
                        self.keys[key_last], self.keys[self.peaks[parent][0]] = \
                            self.keys[self.peaks[parent][0]], self.keys[key_last]  # меняем местами их индексы

                        index = self.keys[key_last]  # обновляем индекс перемещенного вверх элеента
                        self.heapify(parent)  # возобновляем св-во кучи относительно перемещенного родителя
                    else:
                        break



    def print(self):
        if len(self.peaks) == 0:
            print('_')
            return
        counter = 2
        counter_lvl = 1
        for i in range(0, len(self.peaks)):
            if i == 0:
                print('[' + str(self.peaks[i][0]) + ' ' + self.peaks[i][1] + ']')
            else:
                if i % 2 != 0:
                    sys.stdout.write('[' + str(self.peaks[i][0]) + ' '
                                     + self.peaks[i][1] + ' ' + str(self.peaks[(i-1)//2][0]) + ']')
                else:
                    sys.stdout.write('[' + str(self.peaks[i][0]) + ' '
                                     + self.peaks[i][1] + ' ' + str(self.peaks[(i-2)//2][0]) + ']')
                if counter_lvl != counter:
                    sys.stdout.write(' ')
                    counter_lvl += 1
                else:
                    sys.stdout.write('\n')
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
            sys.stdout.write('_ ' * (amount - 1))
            sys.stdout.write('_\n')


def process(heap: Heap, command):
    if command == ' ':
        return
    if re.fullmatch(r'add [-]?[\d+]+ [^\s+]+', command) is not None:
        pos1 = text[4:].find(' ')
        key = int(text[4:pos1 + 4])
        index = heap.find(key)
        if index is None:
            value = command[pos1+5:]
            heap.add(key, value)
        else:
            print('error')
        return
    if re.fullmatch(r"set [-]?[\d+]+ [^\s+]+", text) is not None:
        pos1 = text[4:].find(' ')
        key = int(text[4:pos1 + 4])
        index = heap.find(key)
        if index is not None:
            value = text[pos1 + 5:]
            heap.set(key, value)
        else:
            print('error')
        return
    if re.fullmatch(r'delete [-]?[\d+]+', text) is not None:
        if len(heap.keys) != 0:
            key = int(text[7:])
            if heap.find(key) is not None:
                heap.delete(key)
            else:
                print('error')
        else:
            print('error')
        return
    if re.fullmatch(r'search [-]?[\d+]+', text) is not None:
        key = int(text[7:])
        index = heap.find(key)
        if index is not None:
            print(1, index, heap.peaks[index][1])
        else:
            print(0)
        return
    if re.fullmatch(r'min', text) is not None:
        if len(heap.keys) != 0:
            heap.min()
        else:
            print('error')
        return
    if re.fullmatch(r'max', text) is not None:
        if len(heap.keys) != 0:
            heap.max()
        else:
            print('error')
        return
    if re.fullmatch(r'extract', text) is not None:
        if len(heap.keys) != 0:
            heap.extract()
        else:
            print('error')
        return
    if re.fullmatch(r'print', text) is not None:
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

