#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Optional


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i]
                                      for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: Optional[int] =
                        None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary containing pagination information.

        Arguments:
        index -- the current start index of the return page
        page_size -- the number of items per page

        Returns:
        A dictionary containing the following key-value pairs:
        - index: the current start index of the return page
        - next_index: the next index to query with
        - page_size: the current page size
        - data: the actual page of the dataset
        """
        assert isinstance(index, int) and index >= 0, "non-negative integer"
        assert isinstance(page_size, int) and page_size > 0, "positive integer"

        dataset = self.indexed_dataset()
        total_items = len(dataset)

        if index >= total_items:
            raise AssertionError("Index out of range")

        data = []
        current_index = index
        while len(data) < page_size and current_index < total_items:
            if current_index in dataset:
                data.append(dataset[current_index])
            current_index += 1

        next_index = current_index if current_index < total_items else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
