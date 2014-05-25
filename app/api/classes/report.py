"""
API for dealing with parsing the reporter app summaries
"""
import json
import operator


class ReportSummary(object):
    summaries = []

    def __init__(self, filepath):
        """
        :param filepath (str)
        """
        self.filepath = filepath
        with open(filepath) as f:
            self.summaries = json.loads(f.read())

    def getSummaryForQuestion(self, question):
        """
        :param question (str): e.g. 'How happy are you?'
        :return summary (dict)
        """
        for summary in self.summaries:
            if summary['question'] == question:
                return summary

    def getTopFive(self, question):
        top_five = []
        summary = self.getSummaryForQuestion(question)
        # work team was a mistake.  This shouldn't go here. But it'll do for now
        if 'Work Team' in summary['answers']:
            del summary['answers']['Work Team']
        sorted_all = sorted(
            summary['answers'].iteritems(),
            key=operator.itemgetter(1)
        )
        sorted_all.reverse()
        for tup in sorted_all[:5]:
            top = {
                'answer': tup[0],
                'amount': tup[1]
            }
            top_five.append(top)

        return top_five
