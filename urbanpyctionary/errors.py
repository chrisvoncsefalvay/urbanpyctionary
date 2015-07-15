# coding=utf-8

class NoResultsError(Exception):
    def __str__(self):
        return("No results have been found for this query.")

class IncorrectResultSetError(Exception):
    def __str__(self):
        return("The result set is malformed.")

class MalformedAPIKey(Exception):
    def __str__(self):
        return("Your API key must be a 50-character alphanumeric string. Please check again.")

class APIError(Exception):
    def __init__(self, response_code, message):
        self.response_code = response_code
        self.message = message

    def __str__(self):
        return("The API returned an error code %i: %s" % (self.response_code, self.message))

class APIUnauthorizedError(APIError):
    def __init__(self):
        self.response_code = 403
        self.message = "Could not authorise you - this is probably an issue with your Mashape API key. " \
                       "Please check whether your API key is correct."

class ConnectionError(Exception):
    def __str__(self):
        return("Could not connect to the API. Most likely, this means your internet connection is down or the server is "
               "unreachable.")