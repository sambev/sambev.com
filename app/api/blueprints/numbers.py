from flask import Blueprint, request, render_template
from app.api.classes.report_summary import ReportSummary
from app.api.classes.reports import ReportsAPI
from dateutil import parser as date_parser

numbers = Blueprint('numbers', __name__,
                    template_folder='templates')

numeric_questions = [
    'How happy are you?',
    'How healthy do you feel?',
    'What did you weigh?',
    'How many steps today?',
    'How many floors?',
    'How many miles'
]


@numbers.record
def set_up(state):
    numbers.summary = ReportSummary('static/data/report-summary.json')
    numbers.report = ReportsAPI('static/data/reporter-export.json')

@numbers.route('/numbers', methods=['GET'])
def number():
    if request.method == 'GET':
        summaries = []
        total = len(numbers.report.reports)
        for question in numeric_questions:
            new_summary = {}
            new_summary['question'] = question
            new_summary['average'] = numbers.summary.getSummary(question)['average']
            new_summary['min'] = numbers.summary.getMin(question)
            new_summary['max'] = numbers.summary.getMax(question)
            summaries.append(new_summary)
        return render_template('numbers.html',
                               summaries=summaries,
                               total=total)
