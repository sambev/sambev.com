import json
from flask import Blueprint, request, render_template, Response
from app.api.classes.report import ReportSummary

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.record
def set_up(state):
    main.report = ReportSummary('static/data/report-summary.json')
    main.summaries = main.report.summaries


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
        for summary in main.summaries:
            if summary['question'] in dumb_questions:
                del main.summaries[main.summaries.index(summary)]
            elif summary['type'] in token_types:
                summary['top_five'] = main.report.getTopFive(
                    summary['question'])

    return render_template('index.html', summaries=main.summaries)
