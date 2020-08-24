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

out = dict()
out_verbose = dict()
total_ids = 10000
score_over_90 = 0

print("Starting off ...")
# iterate over all ES ids
for id in range (0,total_ids):
    # construct query
    search_param = {
        # "_source": ["title","abstract","doi","year"],
        "query": {
            "more_like_this": {
                "fields": [ "title", "abstract", "keywords"],
                "like": [
                    {
                    "_index": "some_index",
                    "_id": str(id)
                    }
                ]
            }
        }
    }

    # run query 
    response = client.search(index="some_index", body=search_param)
    # print(response)

    # desconstruct response
    took = response["took"]
    max_score = response["hits"]["max_score"]
    hits_no = response["hits"]["total"]["value"]
    hits = response["hits"]["hits"]
    temp = []

    for hit in hits:
        # save score
        score = hit["_score"]
        temp.append(score)

    out[id] = temp
    # print(temp)

print("\nSaving ES responses to file: sim_scores_"+str(total_ids)+".json") 
with open('sim_scores_'+str(total_ids)+'.json', 'w') as outfile:
    json.dump(out, outfile)
