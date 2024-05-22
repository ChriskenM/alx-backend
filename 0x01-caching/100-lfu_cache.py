#!/usr/bin/env python3
"""
LFU Caching module
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache defines a LFU caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.freqs = defaultdict(int)  # Frequency of access for each key
        self.keys_by_freq = defaultdict(OrderedDict)  # Keys order by freq &use

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self._update_freq(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self._evict()
            self.cache_data[key] = item
            self.freqs[key] = 1
            self.keys_by_freq[1][key] = None

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None
        self._update_freq(key)
        return self.cache_data[key]

    def _update_freq(self, key):
        """ Update the frequency of a key """
        freq = self.freqs[key]
        del self.keys_by_freq[freq][key]
        if not self.keys_by_freq[freq]:
            del self.keys_by_freq[freq]
        self.freqs[key] += 1
        new_freq = self.freqs[key]
        self.keys_by_freq[new_freq][key] = None

    def _evict(self):
        """ Evict the least frequently used item """
        min_freq = min(self.keys_by_freq)
        lru_key, _ = self.keys_by_freq[min_freq].popitem(last=False)
        if not self.keys_by_freq[min_freq]:
            del self.keys_by_freq[min_freq]
        del self.cache_data[lru_key]
        del self.freqs[lru_key]
        print("DISCARD: {}".format(lru_key))
