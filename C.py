import sys
import re

class Heap:

    def __init__(self):
        self.peaks = []
        self.keys = {} # мапа из ключей и индексов для получения за константу

    def heapify(self, index):
        left = 2*index
        right = 2*index + 1
        minimum = index
        if (left < len(self.peaks)) and (self.peaks[left][0] < self.peaks[minimum][0]):
            minimum = left
        if (right < len(self.peaks)) and (self.peaks[right][0] < self.peaks[minimum][0]):
            minimum = right
        if minimum is not index:
            self.peaks[index], self.peaks[minimum] = self.peaks[minimum], self.peaks[index]
            self.heapify(minimum)

    def make_heap(self):
        for i in range(int(len(self.peaks)/2)-1, -1):
            self.heapify(i)

    def find(self, key):
        for i in range(0, len(self.peaks)):
            if self.peaks[i][0] == key:
                return i
        return None

    def set(self, key, value):
        self.peaks[key][1] = value

    def add(self, key, value):
        self.peaks.append((key, value))
        index = len(self.peaks) - 1
        self.keys[key] = index
        while (index > 0) and (self.peaks[int(index/2)][0] > self.peaks[index][0]):
            self.peaks[index], self.peaks[int(index/2)] = self.peaks[int(index/2)], self.peaks[index]
            index = int(index/2)

    def min(self):
        print(self.peaks[0][0], 0, self.peaks[0][1])

    def max(self):
        index_max = max(self.keys, key=self.keys.get)
        print(self.peaks[index_max][0], index_max, self.peaks[index_max][1])

    def extract(self):
        print(self.peaks[0][0], self.peaks[0][1])
        index = len(self.peaks)-1
        key = self.peaks[0][0]
        self.peaks[0] = self.peaks[index]
        del self.peaks[index:index+1]
        del self.keys[key]
        self.heapify(0)

    def delete(self, key):
        if key == self.peaks[len(self.peaks)-1][0]:
            index = len(self.peaks) - 1
            del self.peaks[index:index+1]
        else:
            index = self.keys[key][1]
            self.peaks[0] = self.peaks[index]
            del self.peaks[index:index+1]
            del self.keys[key]
            self.heapify(index)


    def print(self):
        if len(self.peaks) == 0:
            print('_')
            return
        counter = 2
        for i in range(0, len(self.peaks)):
            if i == 0:
                print('[' + str(self.peaks[i][0]) + ' ' + self.peaks[i][1] + ']')
            else:
                if i % 2 == 0:
                    sys.stdout.write('[' + str(self.peaks[i][0]) + ' '
                                     + self.peaks[i][1] + ' ' + str(self.peaks[int(i/2)][0]) + ']')
                else:
                    sys.stdout.write('[' + str(self.peaks[i][0]) + ' '
                                     + self.peaks[i][1] + ' ' + str(self.peaks[int(i-1/2)][0]) + ']')
                if i is not counter:
                    sys.stdout.write(' ')
                else:
                    sys.stdout.write('\n')
                    counter *= 2
        a = 0
        size1 = size2 = len(self.peaks)
        while size1 > 1:
            size1 = int(size1 / 2)
            a += 1
        a += 1
        power = pow(2, a)
        amount = size2 - power
        sys.stdout.write('_ ' * amount)
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
        key = int(text[7:])
        if heap.find(key) is not None:
            heap.delete(key)
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
