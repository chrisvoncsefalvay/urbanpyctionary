#!/usr/bin/env python
#  coding=utf-8

import sys, os
import click
from urbanpyctionary.client import Client
from urbanpyctionary.errors import NoResultsError

@click.command()
@click.option("--apikey", default=None, help="Mashape/Urban Dictionary API key")
@click.argument("search_term")
def search(search_term, apikey):
    key = os.getenv("URBANDICTIONARY_APIKEY", None) if os.getenv("URBANDICTIONARY_APIKEY", None) != None else apikey
    if key is None:
        print("No API key found in the environment variables and none provided.")
        sys.exit(1)
    else:
        print("Querying Urban Dictionary for %s..." % search_term)
        try:
            r = Client(API_key=key).get(search_term)
        except NoResultsError:
            print("No results found for %s." % search_term)
            sys.exit(1)

    print("%i results found for %s. \n" % (len(r), search_term))

    for each in r.definitions:
        print(str(each))
        print("\n")
    sys.exit(0)

if __name__ == '__main__':
    search()
