import unittest
from app.services.sleepapp import SleepAppService
from config.settings import SETTINGS
from pymongo import MongoClient

class SleepAppServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = SleepAppService()
        config = SETTINGS['test']
        self.client = MongoClient(config['DB_URI'])
        self.db = self.client[config['DB_NAME']]
        self.collection = self.db[config['SLEEP_COLLECTION']]
        self.service.save_data_from_file('sleepdata.csv')

    def tearDown(self):
        self.db.drop_collection(self.collection)

    def test_instantiation(self):
        self.assertIsInstance(self.service, SleepAppService)

    def test_can_save_data_to_db(self):
        saved = self.collection.find({})

        self.assertEquals(188, len([s for s in saved]))

    def test_saved_data_has_correct_keys(self):
        saved = self.collection.find({})
        first = [s for s in saved][0]

        self.assertTrue('start' in first)
        self.assertTrue('end' in first)
        self.assertTrue('quality' in first)
        self.assertTrue('time' in first)
        self.assertTrue('wakeup' in first)
        self.assertTrue('notes' in first)
        self.assertTrue('heart_rate' in first)
        self.assertTrue('activity' in first)


    def test_get_summary(self):
        summary = self.service.get_quality_summary()

        self.assertEquals(summary['low'], 39)
        self.assertEquals(summary['average'], 76)
        self.assertEquals(summary['high'], 100)
        self.assertEquals(summary['current'], 89)


if __name__ == '__main__':
    unittest.main()
