#!/usr/bin/env python3
"""
Module for LIFO caching
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    defines a LIFO caching sys
    """
    def __init__(self):
        """initalizes"""
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """adds item to the cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                if self.last_key is not None:
                    del self.cache_data[self.last_key]
                    print("DISCARD: {}".format(self.last_key))
            self.last_key = key

    def get(self, key):
        """gets an item by key
        """
        return self.cache_data.get(key, None)
