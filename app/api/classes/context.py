import numpy as np


class Context(object):

    def __init__(self):
        self.answer = ''
        self.amount = 0
        self.questions = {}
        self.battery = None
        self.audio = None
        self.weather = None
