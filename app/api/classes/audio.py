import numpy as np


class AudioData(object):

    def __init__(self, data):
        self.data = data
        self.avg_avg = np.mean([a['avg'] for a in self.data])
        self.avg_min = min([a['avg'] for a in self.data])
        self.avg_max = max([a['avg'] for a in self.data])
        self.peak_avg = np.mean([a['peak'] for a in self.data])
        self.peak_min = min([a['peak'] for a in self.data])
        self.peak_max = max([a['peak'] for a in self.data])

    def getAverageAudio(self):
        """
        @return {tuple} first index is avg, second is peak
        """
        return (self.avg_avg, self.avg_peak)

    def to_json(self):
        return {
            'data': self.data,
            'avg_avg': self.avg_avg,
            'avg_min': self.avg_min,
            'avg_max': self.avg_max,
            'peak_avg': self.peak_avg,
            'peak_min': self.peak_min,
            'peak_max': self.peak_max
        }
