#!/usr/bin/env python3
"""
LRU cache module
"""
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """
    defines a LRU caching sys
    """
    def __init__(self):
        """initalizes
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """adds an item to the cahe
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded_key = next(iter(self.cache_data))
            print("DISCARD: {}".format(discarded_key))
            self.cache_data.pop(discarded_key)

    def get(self, key):
        """gets items by key
        """
        if key is None or key not in self.cache_data:
            return None
        self.cache_data.move_to_end(key)
        return self.cache_data[key]
