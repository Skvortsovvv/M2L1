import sys


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
        pass


if __name__ == '__main__':

    m = []
    m.append((1, 'qwe'))
    print(m[0][1])

    pass

