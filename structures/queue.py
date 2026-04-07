# Valeria Pérez Alonso A00833973
# Queue implementation using a list
# FIFO - First In First Out

"""
Methods:
    enqueue(item): void
    dequeue(): item
    front(): item
    is_empty(): boolean
    size(): number
    __str__(): string
"""

class Queue:
    def __init__(self):
        """Initializes an empty queue."""
        self.queue = []
    
    def enqueue(self, item):
        """Adds an item to the end of the queue."""
        self.queue.append(item)
    
    def dequeue(self):
        """Removes and returns the first item in the queue. Returns None if the queue is empty."""
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            return None
    
    def front(self):
        """Returns the first item in the queue without removing it. Returns None if the queue is empty."""
        if not self.is_empty():
            return self.queue[0]
        else:
            return None
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
    def __str__(self):
        """Returns a string representation of the queue."""
        return str(self.queue)