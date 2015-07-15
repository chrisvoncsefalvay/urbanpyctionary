About
-----

UrbanPyctionary is a Python package that allows you to query the Urban Dictionary 'secret' API. This is an indirect API
offered through Mashape, and as such, you will need an application-specific Mashape credential.

**Urban Dictionary contains a goodly amount of the crude, rude, racially/sexually/otherwise offensive and the downright
nasty.** The author of this package does not endorse any of the content on Urban Dictionary, but believes it to be a
very interesting window on current linguistic trends and an invaluable research tool. Corpus linguistics expects you to
have a reasonably thick skin and not blush too easily. This package was **created for research purposes only**, and you
should **not** use it for illegal, improper, offensive or discriminatory conduct. No such use is endorsed or approved by
the package author.


Installation
------------

With `pip`::

  $> pip install urbanpyctionary


Usage
-----

To use UrbanPyctionary, you will require a Mashape API key *specifically for the 'Urban Dictionary Unofficial Secret
API'*. Go `here <https://www.mashape.com/community/urban-dictionary>`__ to obtain an API key.

Once you have an API key, create a client object::

    from urbanpyctionary.client import Client

    c = client(API_key = "BwiftJvEbDTs1M7pO3bGeztgJU709eoIufUmDXr8pDdYK5A0K3")


Querying
========

The client object has one main method, ``get(search_term)``, which allows you to query for a search term::

    >>> r = c.get("python")
    <urbanpyctionary Result for python>

If all is well, a ``Result`` object is returned. This object is both a container for the result and an iterable that
allows quick iterative access to individual definitions.


Individual definitions
======================

A ``Result`` object contains a number of indexed definitions. These can be accessed by direct indexing::

    >>> r.definitions[1]
    <urbanpyctionary Definition 4826760 for python>

Alternatively, you can simply use the convenience indexing of the ``Result`` object::

    >>> r[1]
    <urbanpyctionary Definition 4826760 for python>

Using the ``browse()`` method allows you to inspect the content of a definition::

    >>> r[1].browse()
    {   'author': 'dan murray',
    'current_vote': '',
    'defid': 1150813,
    'definition': 'A great little language invented by Guido "the man" van '
                  'Rossum. John Carmack "swears by it", he wrote the Quake 2 '
                  'engine in it!',
    'example': 'print "nohtyp"[::-1]',
    'permalink': 'http://python.urbanup.com/1150813',
    'thumbs_down': 50,
    'thumbs_up': 118,
    'word': 'python'}

