# coding=utf-8

from collections import deque
from threading import Semaphore


class Queue:
    def push(self, obj, **kwargs):
        raise NotImplemented

    def pop(self, **kwargs):
        raise NotImplemented

    def __len__(self):
        raise NotImplemented


class FifoQueue(Queue):
    def __init__(self):
        self._queue = deque()
        self._semaphore = Semaphore(0)

    def push(self, obj, **kwargs):
        self._queue.append(obj)
        self._semaphore.release()

    def pop(self, **kwargs):
        self._semaphore.acquire()
        return self._queue.popleft()

    def __len__(self):
        return len(self._queue)
