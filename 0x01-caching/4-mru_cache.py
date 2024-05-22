#!/usr/bin/env python3
"""
MRU caching module
"""
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """
    defines a MRU cache sys
    """
    def __init__(self):
        """"initialize"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """adds an item to cache
        """
        if key is None and item is None:
            return
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # discards most recently used item
            discarded_key, _ = self.cache_data.popitem(last=True)
            print("DISCARD: {}".format(discarded_key))

    def get(self, key):
        """gets items by key
        """
        if key is None or key not in self.cache_data:
            return None
        self.cache_data.move_to_end(key)
        return self.cache_data[key]
