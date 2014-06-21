import os
import unittest
from app.api.classes.report_summary import ReportSummary
import datetime


class ReportSummaryTest(unittest.TestCase):

    def setUp(self):
        self.summary = ReportSummary('./test_summary.json')
        pass

    def tearDown(self):
        pass

    def testInit(self):
        """Should be able to initialize the ReportSummary object"""
        self.assertEquals(self.summary.filepath, './test_summary.json')

    def testGetTopFive(self):
        """Should be able to get the top 5 of a metric"""
        question = 'Who are you with?'
        self.assertEquals(
            [
                {
                    'answer': 'Marcos',
                    'amount': 175
                },
                {
                    'answer': 'Dean Cheesman',
                    'amount': 148
                },
                {
                    'answer': 'Sean Brown (null)',
                    'amount': 109
                },
                {
                    'answer': 'natalie landrey',
                    'amount': 84
                },
                {
                    'answer': 'Deanna Dillard',
                    'amount': 62
                }
            ],
            self.summary.getTopFive(question)
        )

    def testGetQuestionMin(self):
        """Should be able to get the min and max of a question"""
        question = 'How happy are you?'
        min = self.summary.getQuestionMin(question)
        self.assertEquals(min[0], 3)
        self.assertEquals(min[1].date(), datetime.date(2014, 03, 14))

    def testGetQuestionMax(self):
        """Should be able to get the min and max of a question"""
        question = 'How happy are you?'
        max = self.summary.getQuestionMax(question)
        self.assertEquals(max[0], 9)
        self.assertEquals(max[1].date(), datetime.date(2014, 2, 7))


if __name__ == '__main__':
    unittest.main()
