from collections import deque
class Queue:
    def __init__(self):
        self.items = deque([])

    def isEmpty(self):
        return self.size() == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.popleft()

    def size(self):
        return len(self.items)
