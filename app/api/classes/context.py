import numpy as np


class Context(object):

    def __init__(self):
        self.answer = ''
        self.amount = 0
        self.questions = []
        self.battery = None
        self.audio = None
        self.weather = None

    def has_question(self, question):
        for q in self.questions:
            if question == q['question']:
                return True
        return False

    def add_question(self, question):
        self.questions.append({
            'question': question,
            'answers': []
        })

    def add_answer(self, question, answer):
        for q in self.questions:
            if question == q['question']:
                has_answer = False
                for a in q['answers']:
                    if answer == a['answer']:
                        has_answer = True
                        a['amount'] += 1
                if not has_answer:
                    q['answers'].append({
                        'answer': answer,
                        'amount': 1
                    });

    def to_json(self):
        return {
            'answer': self.answer,
            'amount': self.amount,
            'questions': self.questions,
            'battery': self.battery.to_json(),
            'audio': self.audio.to_json(),
            'weather': self.weather.to_json()
        }
