import json
from app.api.classes.context import Context
from app.api.classes.battery import BatteryData
from app.api.classes.audio import AudioData
from app.api.classes.weather import WeatherData

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
        battery_data = []
        audio_data = []
        weather_data = []
        for report in self.reports:
            if self._reportHasAnswer(report, answer):
                context.amount += 1
                battery_data.append(report['battery'])
                audio_data.append(report['audio'])
                if 'weather' in report:
                    weather_data.append(report['weather'])
                for resp in report['responses']:
                    question = resp['questionPrompt']
                    if not context.has_question(question):
                        context.add_question(question)
                    if 'tokens' in resp:
                        for token in resp['tokens']:
                            if token != answer:
                                context.add_answer(question, token)
                    elif 'locationResponse' in resp:
                        location = resp['locationResponse']['text']
                        if answer != location:
                            context.add_answer(question, location)
        context.battery = BatteryData(battery_data)
        context.audio = AudioData(audio_data)
        context.weather = WeatherData(weather_data)
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
