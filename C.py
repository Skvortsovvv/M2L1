import sys


class Heap:

    def __init__(self):
        self.peaks = []

    def heapify(self, index):
        left = 2*index
        right = 2*i + 1
        largest = index
        if (left < len(self.peaks)) and (self.peaks[left] < self.peaks[largest]):
            largest = left
        if (right < len(self.peaks)) and (self.peaks[right] < self.peaks[largest]):
            largest = right
        if largest is not i:
            self.peaks[index], self.peaks[largest] = self.peaks[largest], self.peaks[index]
            self.Heapify(largest)

    def make_heap(self):
        size = len(self.peaks)
        for i in range(len(self.peaks), -1):
            pass

if __name__ == '__main__':
    pass

