#!/usr/bin/env python3
"""
FIFO caching module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    defines a FIFO caching system
    """

    def __init__(self):
        """intializes
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """adds an item into the caache
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                self.order.append(key)
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                first_key = self.order.pop(0)
                del self.cache_data[first_key]
                print("DISCARD: {}".format(first_key))

    def get(self, key):
        """gets an item by key
        """
        return self.cache_data.get(key, None)
