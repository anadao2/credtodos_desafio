#!/usr/bin/env python3

from pymongo import MongoClient


class Mongo:

    def __init__(self):
        self._client = MongoClient('localhost', 27017)
        self._db = self._client.credtodos

    @property
    def db(self):
        return self._db
