#!/usr/bin/python2.7
# coding=utf-8

import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

"""
    NOTE: This code was generated for the SpringerNature Hackday London to mine metadata 
          for conference proceedings. This script was written in a desperate attempt to get 
          things done in a short time. 
"""

# Set the SPARQL endpoint
sparql = SPARQLWrapper("http://10.101.127.159:7200/repositories/snhackday")

def mine_metadata():
    """Mines metadata from Scigraph"""
    with open('crypto.json') as json_file:  
        conferences = json.load(json_file)
        for indx, conference in enumerate(conferences['results']['bindings']):
            
            try:
                # Instantiate a dictionary to store metadata about a specific paper
                metadata = {}

                """For every conference, grab the relevant metadata"""
                document_identifier = conference['doi']['value']
                SPARQL_stmt = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX sg:<http://scigraph.springernature.com/ontologies/core/>
                    select * where { 
                        ?bc sg:doi '%s' .
                        ?bc sg:title ?t .
                        ?bc sg:doi ?doi .
                        ?bc sg:hasContribution ?contr .
                        ?bc sg:hasBook ?b .
                        ?b sg:hasBookEdition ?be .
                        ?be sg:copyrightYear ?yearpr .
                        ?be sg:copyrightHolder ?nameconf .
                        ?contr sg:publishedName ?name .
                        ?contr sg:hasAffiliation ?dep .
                        ?dep sg:publishedName ?depname
                    } limit 100
                """ % document_identifier
                sparql.setQuery(SPARQL_stmt)
                sparql.setReturnFormat(JSON)
                conferences = sparql.query().convert()
                authors = conferences["results"]["bindings"]

                # Package data into dictionary for each paper
                metadata["title"] = authors[0]["t"]["value"]
                metadata["year"] = authors[0]["yearpr"]["value"]
                metadata["doi"] = authors[0]["doi"]["value"]
                metadata["conference"] = authors[0]["nameconf"]["value"]
                
                metadata["authors"] = []
                for author in authors:
                    author_info = dict()
                    author_info["name"] = author["name"]["value"]
                    author_info["affiliation"] = author["depname"]["value"]
                    metadata["authors"].append(author_info)

                # Now write the dictionary to a file one line at a time
                with open('crytoconf.txt', 'a') as the_file:
                    the_file.write('%s\n' % str (metadata))

                print "%s: %s" % ((indx + 1), authors[0]["doi"]["value"])

            except: # This is bad stuff
                print "missing data!"

            # break # stop after one run

if __name__ == '__main__':
    # Initiate the mining process
    mine_metadata()