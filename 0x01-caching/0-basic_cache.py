#!/usr/bin/env python3
"""
Module for basic cahing
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    Defines a basic cahing system without limit
    """

    def put(self, key, item):
        """adds an item to cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Gets an item by key
        """
        return self.cache_data.get(key, None)
