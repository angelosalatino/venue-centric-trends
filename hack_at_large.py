
import json
import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError


TARGET_INDEX = "scigraph"


def clean_string(string):
    return string.replace('"', '').replace('^^<http://www.w3.org/2001/XMLSchema#gYear>', '')


def main():
    es = Elasticsearch()
    with open('./query-result.tsv') as infile:
        for line in infile:
            paper = {}
            cols = line.split('\t')
            paper['doi'] = clean_string(cols[0])
            authors = cols[1]
            authors = authors[1:len(authors)-1].replace('\\"','"') # horrible replace of spqrl chars
            try:
                paper['author'] = json.loads(authors)
            except json.decoder.JSONDecodeError:
                print('skipping')
                continue
            paper['title'] = clean_string(cols[2])
            paper['conf_name'] = clean_string(cols[3])
            paper['conf_subtitle'] = clean_string(cols[4])
            paper['rights'] = clean_string(cols[5])
            year = clean_string(cols[6])
            paper['year'] = datetime.date(int(year), 1, 1)
    
            es.index(index=TARGET_INDEX, id=paper['doi'], doc_type=TARGET_INDEX, body=paper)

if __name__ == "__main__":
    main()
