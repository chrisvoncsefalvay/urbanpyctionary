"""
UrbanPyctionary: the Python Urban Dictionary Client
(c) Chris von Csefalvay, 2015.

client.py
Declares various objects that wrap concepts in the API wrapper.
"""

__version__ = "0.86"

from datetime import datetime
import requests
import pprint
from urbanpyctionary import errors

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Browsable(object):

    def browse(self):
        pprint.PrettyPrinter(indent=4).pprint(self.result)


class Definition(Browsable):
    """
    A class representing the definition of a term.
    """
    def __init__(self, definition, time_acquired=None):
        """
        Inits a class representing the definition of a term.

        :param definition: A dict containing the API return
        :type definition: dict
        :param time_acquired: Date/time object of acquisition, normally inherited from parent Result object
        :type time_acquired: datetime
        """

        self.result = definition
        self.defid = definition["defid"]
        self.word = definition["word"]
        self.author = definition["author"]
        self.permalink = definition["permalink"]
        self.definition = definition["definition"]
        self.example = definition["example"]
        self.thumbs_up = definition["thumbs_up"]
        self.thumbs_down = definition["thumbs_down"]
        self.time_acquired = time_acquired

    def __repr__(self):
        return("<urbanpyctionary Definition %i for %s>" % (self.defid, self.word))


    def __str__(self):
        return(bcolors.UNDERLINE + bcolors.OKBLUE + "{word} ({defid}, by {author} - {up} up, {down} down).".format(word = self.word,
                                                                                                                   defid = self.defid,
                                                                                                                   author = self.author,
                                                                                                                   up = self.thumbs_up,
                                                                                                                   down = self.thumbs_down) +
        bcolors.ENDC + bcolors.ENDC +"\n"+
        bcolors.OKGREEN + self.definition + bcolors.ENDC + "\n" +
        bcolors.UNDERLINE + "\nExample:\n" + bcolors.ENDC + bcolors.OKBLUE + self.example + bcolors.ENDC + "\n(permalink: " +
        bcolors.UNDERLINE + bcolors.OKBLUE + self.permalink + bcolors.ENDC + bcolors.ENDC + ")")


class Result(Browsable):
    """
    A class representing a result set.
    """
    def __init__(self, result_object):
        self.result = result_object
        if len(result_object) < 1:
            raise errors.IncorrectResultSetError

        try:
            self.tags = result_object["tags"]
            self.result_type = result_object["result_type"]
            self.sounds = result_object["sounds"]
            self.time_acquired = datetime.now()
            self.definitions = [Definition(json_object, self.time_acquired) for json_object in result_object["list"]]
            self.word = self.definitions[0].word
        except KeyError:
            raise errors.IncorrectResultSetError

    def __repr__(self):
        return("<urbanpyctionary Result for %s>" % self.word)

    def __getitem__(self, item):
        return self.definitions[item]

    def __len__(self):
        return len(self.definitions)


class Client(object):
    def __init__(self, API_key=None):
        try:
            if len(API_key) is 50 and isinstance(API_key, str) and API_key != None:
                self.api_key = API_key
            else:
                raise errors.MalformedAPIKey
        except TypeError:
            raise errors.MalformedAPIKey

    def __repr__(self):
        return("<urbanpyctionary Client object>")

    def get(self, word):
        """
        Obtains the definition of a word from Urban Dictionary.

        :param word: word to be searched for
        :type word: str
        :return: a result set with all definitions for the word
        """

        url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=%s" % word

        try:
            res = requests.get(url,
                               headers = {"X-Mashape-Key": self.api_key,
                               "Accept": "text/plain"})
        except requests.ConnectionError:
            raise errors.ConnectionError

        if res.status_code == 200:
            if res.json()["result_type"] == 'no_results':
                raise errors.NoResultsError
            else:
                return Result(res.json())
        else:
            if res.status_code == 403:
                raise errors.APIUnauthorizedError