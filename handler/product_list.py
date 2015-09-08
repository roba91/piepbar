#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import logging
from remote import get_products


class ProductList():
    def __init__(self, *args, **kwargs):
        self.idle = threading.Event()
        self.idle.set()
        self.data = {}  # {data: (name, price)}
        self.update()

    def update(self):
        logger = logging.getLogger("product_list:update")
        """
        Tries to update the ProductList.
        Returns True on success, False otherwise.
        """
        logger.info("fetching data")
        new_values = get_products()
        self.idle.wait()
        if new_values:
            self.data = new_values
            logger.info("fetching done")
            return True
        else:
            logger.error("fetching failed")
            return False

    def get_name(self, obj_id):
        return self.data[obj_id][0]

    def get_price(self, obj_id):
        return self.data[obj_id][1]

    def get_url(self, obj_id):
        return self.data[obj_id][2]

    def contains(self, obj):
        return obj in self.data


PRODUCT_LIST = ProductList()
