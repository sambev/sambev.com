import json
from flask import Blueprint, request, render_template, Response
from app.api.classes.report_summary import ReportSummary
from app.api.classes.reports import ReportsAPI

main = Blueprint('main', __name__,
                 template_folder='templates')


numeric_questions = [
    'How happy are you?',
    'How healthy do you feel?',
    'What did you weigh?',
    'How many steps today?',
    'How many floors?',
    'How many miles'
]


@main.record
def set_up(state):
    main.summary = ReportSummary('static/data/report-summary.json')
    main.reports = ReportsAPI('static/data/reporter-export.json')
    main.summaries = main.summary.summaries


@main.route('/', methods=['GET'])
def index():
    """ Render the landing page """
    if request.method == 'GET':
        token_types = ['tokens', 'choice', 'location']
        dumb_questions = [
            'Are you working?',
            'What music did you listen to?',
            'How did you sleep?',
            'Who did you get to know today?',
            'How many coffees did you have today?'
        ]
        summaries = []
        total = len(main.reports.reports)

        for question in numeric_questions:
            new_summary = {}
            new_summary['question'] = question
            new_summary['average'] = main.summary.getSummary(question)['average']
            new_summary['min'] = main.summary.getMin(question)
            new_summary['max'] = main.summary.getMax(question)
            summaries.append(new_summary)

        for summary in main.summaries:
            if summary['question'] in dumb_questions:
                del main.summaries[main.summaries.index(summary)]

    return render_template('index.html', summary=main.summaries,
                           summaries=summaries,
                           total=total)
