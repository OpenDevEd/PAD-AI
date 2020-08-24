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
html = "<head><style>span {color: red;} em {font-style: normal; color: black;}</style></head><body>"

# iterate over all ES ids
for id in range (0,total_ids):
    found = False
    # construct query
    search_param = {
        # "_source": ["title","abstract","doi","year"],
        "query": {
            "more_like_this": {
                "fields": [ "title", "abstract", "year"],
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

    # desconstruct response
    took = response["took"]
    max_score = response["hits"]["max_score"]
    hits_no = response["hits"]["total"]["value"]
    hits = response["hits"]["hits"]
    temp = []
    orig_record = client.search(index="some_index", body={"query": { "ids" : { "values" : [str(id)] } } })
    temp.append(orig_record)
    orig_title = orig_record["hits"]["hits"][0]["_source"]["title"]
    orig_year = orig_record["hits"]["hits"][0]["_source"]["year"]
    orig_abstract = orig_record["hits"]["hits"][0]["_source"]["abstract"]

    for hit in hits:
        # save score
        score = hit["_score"]
        # temp.append(score)

        year = hit["_source"]["year"]

        sim_id = hit["_id"]
        sim_score = hit["_score"]


        # save title
        # title = hit["_source"]["title"]

        if score > 90 and found == False:
            found = True
            score_over_90 += 1
            # out_verbose[id] = hit

            # title highlighting
            temp_search_param = {
                "_source": ["title"],
                "query": {
                    "match": {
                        "title": orig_title
                    }
                },
                "highlight": {
                    "fields": {
                        "title":  {"number_of_fragments" : 0}
                    }
                }
            }
            highlight_response = client.search(index="some_index", body=temp_search_param)
            highlighted = highlight_response["hits"]["hits"][1]["highlight"]["title"][0]
            html += "<div>ORIGINAL ID: " + str(id) + ", SIMILAR TO ID: " + str(sim_id) + ", SCORE: " + str(sim_score) + "</div></br>"

            html += "<div>" + orig_title + "</div><br/><span>" + highlighted + "</span><br/>"

            # year highlighting
            # year = highlight_response["hits"]["hits"][1]["_source"]["year"]
            html += "<br/><div>" + orig_year + "</div><br/>"
            if int(orig_year) != int(year):
                html += "<span>" + orig_year + "</span><br/>"
            else:
                html += "<span><em>" + year + "</em></span><br/>"

            # abstract highlighting
            temp_search_param = {
                "_source": ["title"],
                "query": {
                    "match": {
                        "abstract": orig_abstract
                    }
                },
                "highlight": {
                    "fields": {
                        "abstract":  {"number_of_fragments" : 0}
                    }
                }
            }
            try:
                highlight_response = client.search(index="some_index", body=temp_search_param)
                highlighted = highlight_response["hits"]["hits"][1]["highlight"]["abstract"][0]
                # print(highlighted)
                html += "<br/><br/><div>" + orig_abstract + "</div><br/><span>" + highlighted + "</span><br/><br/>" 
            except:
                print("Hmm smth wrong with ids: " + str(id) + " vs " + str(sim_id) )    
            html += "<hr>"

            # print(orig_title)
            # print(html)
            # print()

            # temp.append(test)

        # if score > 50:
        #     score_over_50 += 1

    # out_verbose[id] = temp
    # print(temp)

# print("\nSaving ES responses to file: over_90s_"+str(total_ids)+".json") 
# with open('over_90s_'+str(total_ids)+'.json', 'w') as outfile:
#     json.dump(out_verbose, outfile)

html += "</body>"
with open('test_'+str(total_ids)+'.html','w') as outfile:
    outfile.write(html)
    
