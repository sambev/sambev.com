from pymongo import MongoClient, ASCENDING
from config.settings import SETTINGS
import csv

class SleepAppService(object):
    """I let you save sleep app data to the database and have the logic that
    surrounds the sleep app data
    """

    def __init__(self):
        config = SETTINGS['dev']
        self.client = MongoClient(config['DB_URI'])
        self.db = self.client[config['DB_NAME']]
        self.collection = self.db[config['SLEEP_COLLECTION']]

    def save_data_from_file(self, filepath):
        """Save sleept data from the exported csv
        :param {string} filepath
        :returns {bool} True if saved, False otherwise
        """
        sleep_data = []
        with open(filepath) as f:
            all_data = csv.reader(f, delimiter=';')

            for entry in all_data:
                if 'Start' in entry: # dont do anything with the first row
                    pass
                else:
                    new_entry = {}
                    new_entry['start'] = entry[0]
                    new_entry['end'] = entry[1]
                    new_entry['quality'] = entry[2]
                    new_entry['time'] = entry[3]
                    new_entry['wakeup'] = entry[4]
                    new_entry['notes'] = entry[5]
                    new_entry['heart_rate'] = entry[6]
                    new_entry['activity'] = entry[7]
                    sleep_data.append(new_entry)

        for data in sleep_data:
            self.collection.save(data)

    def get_quality_summary(self):
        """Get the quality summary values from all of the data
        :example:  XXX values are in %
        {
            'low': 58,
            'average': 75,
            'high': 100,
            'current': 87
        }
        """
        cur = self.collection.find({}, { 'quality': 1, '_id': 0 })
        all_data = [int(found['quality'].strip('%')) for found in cur]
        summary = {
            'low': min(all_data),
            'high': max(all_data),
            'current': all_data[-1],
            'average': sum(all_data) / len(all_data)
        }

        return summary
