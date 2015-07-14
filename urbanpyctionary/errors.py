class NoResultsError(Exception):
    def __str__(self):
        return("No results have been found for this query.")