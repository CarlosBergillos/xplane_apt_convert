class BIterator:
    def __init__(self, seq):
        self._seq = seq
        self._idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._idx += 1

        if self._idx >= len(self._seq):
            self._idx -= 1
            raise StopIteration()

        return self._seq[self._idx]

    def unnext(self):
        self._idx -= 1

        if self._idx < -1:
            self._idx += 1
            raise IndexError("Can't go back any further.")

    def has_next(self):
        return self._idx < (len(self._seq) - 1)
