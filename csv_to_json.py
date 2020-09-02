import csv
import json

csvfile = open('data/ode_test_10k.csv', 'r')
jsonfile = open('data/ode_test_10k.json', 'w')

#fieldnames = ("id", "year", "title", "authors", "keywords", "abstract", "tak", "importedfrom", "recordmetadata_zbuamajorversion", "recordmetadata_dateretrieved", "recordmetadata_dateconverted", "recordmetadata_recordtype", "recordmetadata_source", "recordmetadata_recordname", "recordmetadata_searchguid", "recordmetadata_numberinsource", "recordmetadata_zbuaminorversion", "publisherdatecopyright", "author100", "location", "daterange", "additionaltitles", "publicationtype", "containername", "doi", "isbn", "links", "citation", "identifier", "itemdatatype", "itemdatahandler", "created_at", "tsv", "tsa", "relevance_score")

reader = csv.DictReader(csvfile)

for row in reader:
    #json.dump({"index" : { "_index" : "test"}}, jsonfile)
    #jsonfile.write('\n')
    json.dump(row, jsonfile)
    jsonfile.write('\n')
jsonfile.write('\n')
