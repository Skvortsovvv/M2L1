import sys
import re

class Heap:

    def __init__(self):
        self.peaks = []

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
        index = self.find(key)
        if index is not None:
            self.peaks[index][1] = value
            return

    def add(self, key, value):
        self.peaks.append((key, value))
        index = len(self.peaks) - 1
        while (index > 0) and (self.peaks[int(index/2)][0] > self.peaks[index][0]):
            self.peaks[index], self.peaks[int(index/2)] = self.peaks[int(index/2)], self.peaks[index]
            index = int(index/2)

    def min(self):
        print(self.peaks[0][0], 0, self.peaks[0][1])

    def max(self):
        a = 0
        size1 = size2 = len(self.peaks)
        while size1 > 1:
            size1 = int(size1/2)
            a += 1
        index = pow(2, a)
        index -= 1
        maximum = None
        for i in range(index, size2):
            if maximum is None:
                maximum = i
            elif self.peaks[i][0] > self.peaks[maximum][0]:
                maximum = i
        print(self.peaks[maximum][0], maximum, self.peaks[maximum][1])

    def extract(self):
        print(self.peaks[0][0], self.peaks[0][1])
        index = len(self.peaks)-1
        self.peaks[0] = self.peaks[index]
        del self.peaks[index:index+1]
        self.heapify(0)

    def delete(self, index):
        self.peaks[index] = self.peaks[len(self.peaks)-1]
        self.heapify(index)

    def print(self):
        counter = 2
        if len(self.peaks) == 0:
            print('_')
            return
        for i in range(0, len(self.peaks)):
            if i == 0:
                print('[' + self.peaks[i][0] + ' ' + self.peaks[i][1] + ']')
            else:
                if i % 2 == 0:
                    sys.stdout.write('[' + self.peaks[i][0] + ' '
                                     + self.peaks[i][1] + ' ' + self.peaks[int(i/2)][0] + ']')
                else:
                    sys.stdout.write('[' + self.peaks[i][0] + ' '
                                     + self.peaks[i][1] + ' ' + self.peaks[int(i-1/2)][0] + ']')
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
    if re.fullmatch(r'add [-]?[\d+]+ [^\s+]+', command):
        pos1 = text[4:].find(' ')
        key = int(text[4:pos1 + 4])
        index = heap.find(key)
        if index is not None:
            value = command[pos1+5:]
            heap.add(key, value)
        else:
            print('error')



if __name__ == '__main__':

    min_heap = Heap()

    while True:
        text = input()
        process(min_heap, text)

    pass

