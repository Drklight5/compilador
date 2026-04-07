# Valeria Pérez Alonso A00833973
# Hash Table implementation using Python dictionary

"""
Methods:
    put(key, value): void
    get(key): value
    remove(key): void
    contains(key): boolean
    size(): number
    is_empty(): boolean
    __str__(): string
"""

class HashTable:
    def __init__(self):
        """Initializes an empty hash table."""
        self.table = {}
    
    def put(self, key, value):
        """Adds or updates a key-value pair."""
        self.table[key] = value
    
    def get(self, key):
        """Returns the value associated with the key. Returns None if the key does not exist."""
        return self.table.get(key, None)
    
    def remove(self, key):
        """Removes a key-value pair. Does nothing if the key does not exist."""
        if key in self.table:
            del self.table[key]
    
    def contains(self, key):
        """Returns True if the key exists, False otherwise."""
        return key in self.table
    
    def size(self):
        """Returns the number of elements in the hash table."""
        return len(self.table)
    
    def is_empty(self):
        return len(self.table) == 0
    
    def __str__(self):
        """Returns a string representation of the hash table."""
        return str(self.table)