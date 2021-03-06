from operator import itemgetter

from pymongo import MongoClient, ASCENDING
from datetime import datetime
import dateutil.parser

from config.settings import SETTINGS


def parse_reporter_date(value):
    """Parse the date from a reporterApp report.  It can be one of two formats
    1. Stupid Apple date that is seconds from 01.01.2001
    2. ISO date YYYY-MM-DDTHH:MM:SS

    :param value {mixed} - float (case 1), string (case 2)
    :returns datetime
    """
    iphone_date = 978307200
    if type(value) == type(0.0):
        return datetime.fromtimestamp(iphone_date + value).replace(tzinfo=None)
    else:
        return dateutil.parser.parse(value).replace(tzinfo=None)


class ReportService(object):

    def __init__(self):
        config = SETTINGS['dev']
        self.client = MongoClient(config['DB_URI'])
        self.db = self.client[config['DB_NAME']]
        self.collection = self.db[config['REPORT_COLLECTION']]

    def get_all_reports(self, sort=ASCENDING):
        return self._query({})

    def _query(self, query, filters=[], sort=ASCENDING):
        """
        @param dict query
        @param List filters
        @return dict data
        """
        query_filter = {item: 1 for (item) in filters}
        query_filter['_id'] = 0

        for filt in filters:
            query_filter[filt] = 1

        data = [d for d in self.collection.find(
            query, query_filter).sort('date', sort)]

        return data

    def get_token_summary(self, question):
        """Get the token summary from the given question
        :param {string} question
        :return {dict}
        """
        query = {
            'responses.questionPrompt': question
        }
        filters = ['responses']
        reports = self._query(query, filters)
        summary = {}

        for report in reports:
            for response in report.get('responses', []):
                if response.get('questionPrompt') == question:
                    tokens = response.get('tokens')
                    if tokens:
                        for token in tokens:
                            if token['text'] != 'Nate Mcbride':
                                if token['text'] not in summary:
                                    summary[token['text']] = 1
                                else:
                                    summary[token['text']] += 1

        return sorted(summary.items(), key=itemgetter(1), reverse=True)

    def get_location_summary(self, question):
        """Get the location summary for the given questionPrompt
        :param {string} question
        :return {dict}
        """
        query = {
            'responses.questionPrompt': question
        }
        filters = ['responses']
        reports = self._query(query, filters)
        summary = {}

        for report in reports:
            for response in report.get('responses', []):
                if response.get('questionPrompt') == question:
                    location = response.get('locationResponse', {}).get('text')
                    if location not in summary:
                        summary[location] = 1
                    else:
                        summary[location] += 1

        return sorted(summary.items(), key=itemgetter(1), reverse=True)

    def get_numeric_summary(self, question):
        """Get all the summary data from all of the reports
        :return {dict} of the summary items
        """
        query = {
            'responses.questionPrompt': question
        }
        filters = ['responses']
        reports = self._query(query, filters)
        data = []
        summary = {
            'total': 0,
            'average': 0,
            'min': 0,
            'max': 0,
            'current': 0
        }

        for report in reports:
            for response in report.get('responses', []):
                if response.get('questionPrompt') == question:
                    if response.get('numericResponse'):
                        summary[
                            'total'] += float(response.get('numericResponse'))
                        data.append(float(response.get('numericResponse')))

        summary['average'] = summary['total'] / len(data)
        summary['min'] = min(data)
        summary['max'] = max(data)
        summary['current'] = data[-1]

        return summary

    def get_report_totals(self):
        totals = {
            'reports': 0,
            'days': 0,
            'avg_per_day': 0,
            'tokens': 0,
            'locations': 0,
            'people': 0
        }

        reports = self.get_all_reports()
        first_date = parse_reporter_date(reports[0].get('date'))
        last_date = parse_reporter_date(reports[-1].get('date'))

        tokens = self.collection.find({
            'responses.tokens.text': {'$exists': True}
        }).distinct('responses.tokens.text')

        locations = self.collection.find({
            'responses.locationResponse.text': {'$exists': True}
        }).distinct('responses.locationResponse.text')

        people = self.collection.find({
            'responses.questionPrompt': 'Who are you with?',
            'responses.tokens.text': {'$exists': True}
        }).distinct('responses.tokens.text')

        totals['reports'] = len(reports)
        totals['tokens'] = len(tokens)
        totals['locations'] = len(locations)
        totals['people'] = len([p for p in people])
        totals['days'] = (last_date - first_date).days
        totals['avg_per_day'] = len(reports) / (last_date - first_date).days
        return totals

    def getReportsByToken(self, question, token, filters=[]):
        """
        @param String token
        @param List filters
        @return dict data
        """
        query = {
            'responses.questionPrompt': question,
            'responses.tokens.text': token
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

    def getGeoJSONData(self, question=None, answer=None):
        """
        @example reponse:
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [125.6, 10.1]
                },
                "properties": {
                    "name": "Dinagat Islands"
                }
            }
        @param String question
        @param String answer
        @return dict data
        """
        location_filter = [
            'location.latitude',
            'location.longitude',
            'responses.locationResponse.text'
        ]

        if question and answer:
            reports = self.getReportsByToken(question, answer, location_filter)
        else:
            reports = self.collection.distinct('responses.locationResponse')

        geo_data = []

        for rep in reports:
            if 'location' in rep:
                new_geo = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [
                            rep['location']['longitude'],
                            rep['location']['latitude']
                        ]
                    },
                    'properties': {}
                }

                if 'responses' in rep:
                    for resp in rep['responses']:
                        if 'locationResponse' in resp:
                            new_geo['properties']['name'] = resp[
                                'locationResponse']['text']

                geo_data.append(new_geo)

        return geo_data

    def get_report_dates(self):
        """Get all the dates that reports were filled out.
        @return List
        """
        dates = self.collection.distinct('sectionIdentifier')
        # the [2:] is to get rid of the leading '1-'
        return [d[2:] for d in dates]

    def get_reports_for_date(self, date):
        """Get all the reports for the given date. Date format is '2014-01-10'
        @param String date
        @return List
        """
        query = {
            'sectionIdentifier': '1-' + date
        }
        reports = self._query(query)

        return [r for r in reports]
