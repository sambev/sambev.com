import json
import numpy as np


class Context(object):

    def __init__(self):
        self.answer = ''
        self.amount = 0
        self.questions = {}
        self.battery_life = []
        self.audio = []
        self.weather = []

    def getAverageBatteryLife(self):
        """
        @return int
        """
        return int(np.mean(self.battery_life) * 100)

    def getAverageTemp(self):
        """
        @return {tuple} First index is F, second is C
        """
        avg_f = np.mean([w['tempF'] for w in self.weather])
        avg_c = np.mean([w['tempC'] for w in self.weather])
        return (avg_f, avg_c)

    def getLowTemp(self):
        """
        @return {tuple} first index is F, second is C
        """
        low_f = min([w['tempF'] for w in self.weather])
        low_c = min([w['tempC'] for w in self.weather])
        return (low_f, low_c)

    def getHighTemp(self):
        """
        @return {tuple} first index is F, second is C
        """
        high_f = max([w['tempF'] for w in self.weather])
        high_c = max([w['tempC'] for w in self.weather])
        return (high_f, high_c)

    def getWindAverage(self):
        """
        @return {float}
        """
        return np.mean([w['windMPH'] for w in self.weather])

    def getWindMin(self):
        """
        @return {float}
        """
        return min([w['windMPH'] for w in self.weather])

    def getWindMax(self):
        """
        @return {float}
        """
        return max([w['windMPH'] for w in self.weather])

    def getAverageAudio(self):
        """
        @return {tuple} first index is avg, second is peak
        """
        avg_avg = np.mean([a['avg'] for a in self.audio])
        avg_peak = np.mean([a['peak'] for a in self.audio])
        return (avg_avg, avg_peak)

    def getAvgAudioMin(self):
        """
        @return {float}
        """
        return min([a['avg'] for a in self.audio])

    def getAvgAudioMax(self):
        """
        @return {float}
        """
        return max([a['avg'] for a in self.audio])

    def getPeakAudioMin(self):
        """
        @return {float}
        """
        return min([a['peak'] for a in self.audio])

    def getPeakAudioMax(self):
        """
        @return {float}
        """
        return max([a['peak'] for a in self.audio])



class ReportsAPI(object):

    def __init__(self, filepath):
        """
        @param filepath (str)
        """
        self.filepath = filepath
        self.questions = []

        with open(filepath) as f:
            report_export = json.loads(f.read())
            self.reports = report_export['snapshots']
            for question in report_export['questions']:
                self.questions.append(question['prompt'])

    def getContext(self, answer):
        """
        @param {string} answer
        @return {Context} context
        """
        context = Context()
        context.answer = answer
        for report in self.reports:
            if self._reportHasAnswer(report, answer):
                context.amount += 1
                context.battery_life.append(report['battery'])
                context.audio.append(report['audio'])
                if 'weather' in report:
                    context.weather.append(report['weather'])
                for resp in report['responses']:
                    question = resp['questionPrompt']
                    if question not in context.questions:
                        context.questions[question] = {}
                    if 'tokens' in resp:
                        for token in resp['tokens']:
                            if token == answer:
                                pass
                            elif token not in context.questions[question]:
                                context.questions[question][token] = 1
                            else:
                                context.questions[question][token] += 1
                    elif 'locationResponse' in resp:
                        location = resp['locationResponse']['text']
                        if answer == location:
                            pass
                        elif location not in context.questions[question]:
                            context.questions[question][location] = 1
                        else:
                            context.questions[question][location] += 1
        return context

    def _reportHasAnswer(self, report, answer):
        """
        @param {string} answer
        @return {bool}
        """
        for res in report['responses']:
            for key in res:
                if key != 'questionPrompt':
                    if key in ['tokens'] and answer in res[key]:
                        return True
                    if key == 'locationResponse' and answer == res[key]['text']:
                        return True
        return False
