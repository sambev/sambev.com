import numpy as np


class WeatherData(object):

    def __init__(self, data):
        self.data = data
        self.avg_f = np.mean([w['tempF'] for w in self.data])
        self.avg_c = np.mean([w['tempC'] for w in self.data])
        self.low_f = min([w['tempF'] for w in self.data])
        self.low_c = min([w['tempC'] for w in self.data])
        self.high_f = max([w['tempF'] for w in self.data])
        self.high_c = max([w['tempC'] for w in self.data])
        self.wind_avg = np.mean([w['windMPH'] for w in self.data])
        self.wind_low = min([w['windMPH'] for w in self.data])
        self.wind_high = max([w['windMPH'] for w in self.data])

    def getAverageTemp(self):
        """
        @return {tuple} First index is F, second is C
        """
        return (self.avg_f, self.avg_c)

    def getLowTemp(self):
        """
        @return {tuple} first index is F, second is C
        """
        return (self.low_f, self.low_c)

    def getHighTemp(self):
        """
        @return {tuple} first index is F, second is C
        """
        return (self.high_f, self.high_c)
