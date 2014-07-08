import unittest
from app.api.report_api import ReportService


class ReportServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = ReportService()

    def tearDown(self):
        pass

    def testInit(self):
        self.assertIsInstance(self.service, ReportService)

    def testGetReportsByToken(self):
        """It should be able to get tokens"""
        reports = self.service.getReportsByToken('Who are you with?', 'Marcos')
        self.assertEquals(len(reports), 245)

    def testGetReportsByTokenSpaces(self):
        """It should be able to handle spaces"""
        reports = self.service.getReportsByToken('Who are you with?', 'Dean Cheesman')
        self.assertEquals(len(reports), 222)

    def testGetReportsByTokenNonExistant(self):
        """It should be able to handle a bad answer"""
        reports = self.service.getReportsByToken('Who are you with?', 'foo bar')
        self.assertEquals(len(reports), 0)

    def testGetReportsByTokenNone(self):
        """It should be able to handle a none response"""
        reports = self.service.getReportsByToken('Who are you with?', None)
        self.assertEquals(len(reports), 0)

    def testGetNumericReports(self):
        """It should be able to get reports by quesiton and value"""
        reports = self.service.getNumericReports('How happy are you?', 10)
        self.assertEquals(len(reports), 21)

    def testGetAnsweredOptions(self):
        """It should be able to get reports by answeredOptions"""
        reports = self.service.getAnsweredOptions('Are you working?', 'Yes')
        self.assertEquals(len(reports), 181)

    def testGetLocationReports(self):
        """It should be able to get reports by locationResponse"""
        reports = self.service.getLocationReports('Where are you?', 'Home apt')
        self.assertEquals(len(reports), 246)

if __name__ == '__main__':
    unittest.main()
