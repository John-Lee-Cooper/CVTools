from typing import Sequence, Any


class RingBuffer:
    """ 
    >>> abc = RingBuffer("abc", "b")
    >>> abc.list, abc.value()
    ('abc', 'b')
    >>> abc.next()
    'c'
    >>> abc.next()
    'a'
    >>> abc.prev()
    'c'
    """

    def __init__(self, list_: Sequence, value: Any = None):
        self.forward = True
        self.list = list(list_)
        self.length = len(self.list)
        self.index = 0 if value is None else self.list.index(value)

    def __repr__(self):
        return f"RingBuffer({self.list}, {self.value()})"

    def __len__(self):
        return self.length

    def __iter__(self):
        return self

    def __next__(self):
        return self.value()

    def value(self) -> Any:
        """ Return the current item in the list """
        if self.length == 0:
            raise StopIteration
        return self.list[self.index]

    def next(self) -> Any:
        """ Advance to the next item in the list and return it """
        self.forward = True
        self.index += 1
        if self.index >= self.length:
            self.index = 0
        return self.value()

    def prev(self) -> Any:
        """ Advance to the previous item in the list and return it """
        self.forward = False
        self.index -= 1
        if self.index < 0:
            self.index = self.length - 1
        return self.value()

    def pop(self) -> Any:
        del self.list[self.index]
        if self.forward:
            if self.index >= self.length:
                self.index = 0
            return self.value()
        else:
            return self.prev()
