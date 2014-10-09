import os
import unittest
from app.entities.reports import ReportsAPI
import datetime


class ReportTest(unittest.TestCase):

    def setUp(self):
        self.api = ReportsAPI('./test_reports.json')
        pass

    def tearDown(self):
        pass

    def testInit(self):
        self.assertIsInstance(self.api, ReportsAPI)
        self.assertEqual(1091, len(self.api.reports))

    def testGetContextAmount(self):
        answer = 'Marcos'
        context = self.api.getContext(answer)
        self.assertEqual(context.amount, 201)

    def testGetContextOtherWhoAreYouWith(self):
        answer = 'Marcos'
        context = self.api.getContext(answer)
        self.assertTrue('Dean Cheesman' in context.questions['Who are you with?'])
        self.assertEqual(len(context.questions['Who are you with?']), 79)

    def test_reportHasAnswer(self):
        report = self.api.reports[0];
        self.assertTrue(self.api._reportHasAnswer(report, 'Work Team'))
        self.assertFalse(self.api._reportHasAnswer(report, 'Work Team fo'))


if __name__ == '__main__':
    unittest.main()
