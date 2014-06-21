import json


class Context(object):

    def __init__(self):
        self.answer = ''
        self.amount = 0
        self.questions = {}


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
                        if location not in context.questions[question]:
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
                if key != 'questionPrompt' and answer in res[key]:
                    return True
        return False

    def _addTokenContext(self, resp, context):
        """
        TESTME: this isn't tested because it kind of sucks to test, which
            is a sign it sucks.
        FIXME: this method kind of sucks and really just breaks up getContext
        """
