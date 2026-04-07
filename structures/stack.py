# Valeria Pérez Alonso A00833973
# Stack implementation using a list
# LIFO - Last In First Out

"""
Methods:
    push(item): void
    pop(): item
    peek(): item
    is_empty(): boolean
    size(): number
    __str__(): string
"""

class Stack:
    def __init__(self):
        """Initializes an empty stack."""
        self.stack = []
    
    def push(self, item):
        """Adds an item to the top"""
        self.stack.append(item)
    
    def pop(self):
        """Removes and returns the item at the top of the stack. Returns None if the stack is empty."""
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None
    
    def peek(self):
        """Returns the item at the top of the stack without removing it. Returns None if the stack is empty."""
        if not self.is_empty():
            return self.stack[-1]
        else:
            return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
    
    def __str__(self):
        """Returns a string representation of the stack."""
        return str(self.stack)  
    