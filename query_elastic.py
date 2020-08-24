#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import Python's JSON library for its loads() method
import json, requests

# import time for its sleep method
from time import sleep

# import the datetime libraries datetime.now() method
from datetime import datetime

# use the Elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers

# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("localhost:9200")

# Python dictionary object representing an Elasticsearch JSON query:
search_param = {
    "_source": ["title","abstract","doi","year"],
    "query": {
        "more_like_this": {
            "fields": [ "title", "abstract", "keywords" ],
            "like": [
                {
                "_index": "some_index",
                "_id": "5632"
                }
            ]
        }
    }
}

print("\nRunning the following query on ES instance:")
print(search_param) 
response = client.search(index="some_index", body=search_param)

print("\nSaving ES response to file: response.json") 
with open('response.json', 'w') as outfile:
    json.dump(response, outfile)

    