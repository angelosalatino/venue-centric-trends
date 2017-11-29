
import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError


TARGET_INDEX = "snhackday"


def clean_string(string):
    return string.replace('"', '').replace('^^<http://www.w3.org/2001/XMLSchema#gYear>', '')


def main():
    es = Elasticsearch()
    papers = {}
    with open('./query-result.tsv') as infile:
        a = 0
        for line in infile:
            # if a == 2000:
            #     break
            cols = line.split('\t')
            doi = clean_string(cols[1])
            title =clean_string(cols[2])
            author_name = clean_string(cols[3])
            org_id = clean_string(cols[4])
            org_name = clean_string(cols[5])
            year = clean_string(cols[6])
            conf_id = clean_string(cols[7])
            conf_name = clean_string(cols[8])
            conf_subtitle = clean_string(cols[9])

            if doi not in papers.keys():
                papers[doi] = {}
                papers[doi]['doi'] = doi
                papers[doi]['year'] = datetime.date(int(year), 1, 1)
                papers[doi]['conf_id'] = conf_id
                papers[doi]['conf_name'] = conf_name
                papers[doi]['conf_subtitle'] = conf_subtitle
                papers[doi]['authors'] = []
                papers[doi]['authors'].append({'name': author_name, 'affiliations': org_name})
            else:
                papers[doi]['authors'].append({'name': author_name, 'affiliations': org_name})
            
            a += 1
    
    # print(papers)
    print('indexing')
    for doi in papers.keys():
        # print(papers[doi])
        es.index(index=TARGET_INDEX, id=doi, doc_type=TARGET_INDEX, body=papers[doi])

if __name__ == "__main__":
    main()
