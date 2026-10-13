"""
CPTR 2265 - Lab 7, Part B (optional starter)
============================================

A simple data structure whose sorting algorithm is chosen with an if/elif
chain on a string. Adding a new algorithm means editing this class, and the
client must know the magic strings.

Your task: apply the STRATEGY pattern so that
  * each sorting algorithm lives in its own class with a common interface
    (e.g. a SortStrategy base class / Protocol with a sort(values) method),
  * NumberCollection receives a strategy (constructor and/or a setter),
  * the client can switch algorithms at runtime WITHOUT changing the code
    inside NumberCollection.

You may use this file, or write your own simple data structure instead.
"""


# --------------------------------------------------------------------------
# Strategy interface
# --------------------------------------------------------------------------

class SortStrategy:
    def sort(self, values):
        raise NotImplementedError


# --------------------------------------------------------------------------
# Sorting strategies
# --------------------------------------------------------------------------

class BubbleSortStrategy(SortStrategy):
    def sort(self, values):
        data = list(values)

        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]

        return data


class MergeSortStrategy(SortStrategy):
    def sort(self, values):
        data = list(values)

        if len(data) <= 1:
            return data

        mid = len(data) // 2

        left = self.sort(data[:mid])
        right = self.sort(data[mid:])

        merged = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged


# --------------------------------------------------------------------------
# Number collection
# --------------------------------------------------------------------------

class NumberCollection:
    def __init__(self, values=None, strategy=None):
        self._values = list(values) if values else []
        self._strategy = strategy

    def add(self, value):
        self._values.append(value)

    def values(self):
        return list(self._values)

    def set_strategy(self, strategy):
        self._strategy = strategy

    def sort(self):
        if self._strategy is None:
            raise ValueError("No sorting strategy has been selected")

        self._values = self._strategy.sort(self._values)


# --------------------------------------------------------------------------
# Client
# --------------------------------------------------------------------------

if __name__ == "__main__":
    nums = NumberCollection(
        [42, 7, 19, 3, 88, 25, 61],
        BubbleSortStrategy()
    )
    nums.sort()
    print("Bubble sort:", nums.values())

    nums = NumberCollection(
        [42, 7, 19, 3, 88, 25, 61],
        MergeSortStrategy()
    )
    nums.sort()
    print("Merge sort: ", nums.values())


