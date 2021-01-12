"""
Generic circular buffer
"""

from typing import Any, Iterator, Sequence, Union


class RingBuffer:
    """
    Generic circular buffer.

    >>> ring = RingBuffer("abc", "b")
    >>> ring.forward()
    >>> str(ring)
    "RingBuffer(['a', 'b', 'c'], 'b')"
    >>> next(ring)
    'c'
    >>> next(ring)
    'a'
    >>> ring.backward()
    >>> next(ring)
    'c'
    """

    def __init__(self, list_: Union[Sequence, Iterator], value: Any = None):
        self._step = 0
        self._list = list(list_)
        self._index = 0 if value is None else self._list.index(value)

    def __repr__(self):
        return f"RingBuffer({self._list}, {repr(self.value())})"

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._list:
            raise StopIteration()

        self._index = (self._index + self._step) % len(self._list)
        return self._list[self._index]

    def value(self) -> Any:
        """
        Return the current item in the list

        >>> ring = RingBuffer("abc", "b")
        >>> ring.value()
        'b'
        """
        if not self._list:
            raise StopIteration
        return self._list[self._index]

    def next_(self) -> Any:
        """ Advance ringbuffer index forward """
        self._index = (self._index + 1) % len(self._list)
        return self._list[self._index]

    def prev_(self) -> Any:
        """ Advance ringbuffer index backward """
        self._index = (self._index - 1) % len(self._list)
        return self._list[self._index]

    def forward(self) -> None:
        """ Cause ringbuffer next call to __next__ to advance forward """
        self._step = 1

    def backward(self) -> None:
        """ Cause ringbuffer next call to __next__ to advance backward """
        self._step = -1

    def stop(self) -> None:
        """ Cause ringbuffer next call to __next__ to not advance """
        self._step = 0

    def pop(self) -> Any:
        """
        Remove the current item in the list and return it.

        >>> ring = RingBuffer("abcd", "c")
        >>> ring.pop()
        'c'
        >>> str(ring)
        "RingBuffer(['a', 'b', 'd'], 'b')"
        >>> ring.backward()
        >>> ring.pop()
        'b'
        >>> str(ring)
        "RingBuffer(['a', 'd'], 'd')"
        """
        result = self._list[self._index]
        del self._list[self._index]
        if self._step >= 0:
            self._index -= 1
        return result
