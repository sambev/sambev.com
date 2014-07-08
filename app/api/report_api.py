from pymongo import MongoClient
from config.settings import SETTINGS


class ReportService(object):

    def __init__(self):
        config = SETTINGS['test']
        self.client = MongoClient(config['DB_URI'])
        self.db = self.client[config['DB_NAME']]
        self.collection = self.db[config['COLLECTION']]

    def getReportsByToken(self, question, token, filters=[]):
        """
        @param String token
        @param List filters
        @return dict data
        """
        query = {
            'responses.questionPrompt': question,
            'responses.tokens': token
        }
        return self._query(query, filters)

    def getNumericReports(self, question, answer=None, filters=[]):
        """
        @param String question
        @param String answer
        @return dict
        """
        query = {'responses.questionPrompt': question}
        if answer:
            query['responses.numericResponse'] = str(answer)
        return self._query(query, filters)

    def getAnsweredOptions(self, question, answer=None, filters=[]):
        query = {'responses.questionPrompt': question}
        if answer:
            query['responses.answeredOptions'] = answer
        return self._query(query, filters)

    def getLocationReports(self, question, answer=None, filters=[]):
        query = {'responses.questionPrompt': question}
        if answer:
            query['responses.locationResponse.text'] = answer
        return self._query(query, filters)

    def _query(self, query, filters=[]):
        """
        @param dict query
        @param List filters
        @return dict data
        """
        query_filter = {item: 1 for (item) in filters}
        query_filter['_id'] = 0
        for filt in filters:
            query_filter[filt] = 1
        data = [d for d in self.collection.find(query, query_filter)]
        return data

