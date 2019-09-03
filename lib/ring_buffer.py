#!/usr/bin/env python

import collections
from typing import Sequence, Any


class RingBuffer:
    """ 
    >>> abc = RingBuffer("abc", "b")
    >>> abc.sequence, abc.value()
    ('abc', 'b')
    >>> abc.next()
    'c'
    >>> abc.next()
    'a'
    >>> abc.prev()
    'c'
    """

    def __init__(self, sequence: Sequence, value: Any = None):
        if not isinstance(sequence, collections.Sequence):
            sequence = tuple(sequence)
        self.sequence = sequence
        self.length = len(sequence)
        self.index = 0 if value is None else sequence.index(value)

    def __len__(self):
        return self.length

    def value(self) -> Any:
        """ Return the current item in the sequence """
        return self.sequence[self.index] if self.length else None

    def next(self) -> Any:
        """ Advance to the next item in the sequence and return it """
        self.index += 1
        if self.index >= self.length:
            self.index = 0
        return self.value()

    def prev(self) -> Any:
        """ Advance to the previous item in the sequence and return it """
        self.index -= 1
        if self.index < 0:
            self.index = self.length - 1
        return self.value()


