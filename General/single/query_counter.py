from django.db import connection


def queryPrint(queries, logPath, nopq=0):

    with open(logPath, 'w') as logPathFile:

        for q in range(nopq, len(queries)):
            querie = queries[q]
            logPathFile.write(
                '\nquery #%s     length-%s\n%s\n--------------------\n' % (q, len(querie['sql'].split(',')), querie)
            )


def queryCounter(logPath):

    # remove to not allow inner function
    # assert connection.queries == []

    def fun(function):

        def context(*args, **kwargs):

            noprequeries = len(connection.queries)

            result = function(*args, **kwargs)

            queryPrint(connection.queries, logPath, noprequeries)

            return result

        return context

    return fun