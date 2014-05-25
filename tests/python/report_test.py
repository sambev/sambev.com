import os
import unittest
from app.api.classes.report import ReportSummary


class BasicTest(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
