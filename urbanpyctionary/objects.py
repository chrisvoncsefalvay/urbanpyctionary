"""
UrbanPyctionary: the Python Urban Dictionary Client
(c) Chris von Csefalvay, 2015.

objects.py
Declares various objects that wrap concepts in the API wrapper.
"""
import json
from datetime import datetime
import requests
from urbanpyctionary import errors


class Definition(object):
    def __init__(self, definition, time_acquired=None):

        self.defid = definition["defid"]
        self.word = definition["word"]
        self.author = definition["author"]
        self.permalink = definition["permalink"]
        self.definition = definition["definition"]
        self.example = definition["example"]
        self.thumbs_up = definition["thumbs_up"]
        self.thumbs_down = definition["thumbs_down"]
        self.time_acquired = time_acquired

class Result(object):
    def __init__(self, result_object):

        self.tags = result_object["tags"]
        self.result_type = result_object["result_type"]
        self.sounds = result_object["sounds"]
        self.time_acquired = datetime.now().isoformat()
        self.definitions = [Definition(json_object, self.time_acquired) for json_object in result_object["list"]]

class Client(object):
    def __init__(self, API_key):
        self.api_key = API_key
        
    def get(self, word):
        try:
            url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=%s" % word
            res = requests.get(url,
                         headers = {"X-Mashape-Key": self.api_key,
                                    "Accept": "text/plain"})
            if json.loads(res.json())["result_type"] is "no_results":
                raise errors.NoResultsError
            else:
                return Result(json.loads(res.json()))
        except Exception as e:
            print(e)