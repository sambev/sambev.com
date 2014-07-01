import numpy as np


class BatteryData(object):

    def __init__(self, data):
        self.data = data
        self.average = int(np.mean(self.data) * 100)

    def to_json(self):
        return {
            'data': self.data,
            'average': self.average
        }
