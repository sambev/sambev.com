from flask import Blueprint, request, render_template
from app.api.classes.report_summary import ReportSummary
from dateutil import parser as date_parser

happy_bp = Blueprint('happy_bp', __name__,
                      template_folder='templates')

@happy_bp.record
def set_up(state):
    happy_bp.report = ReportSummary('static/data/report-summary.json')

@happy_bp.route('/happiness', methods=['GET'])
def happiness():
    if request.method == 'GET':
        question = 'How happy are you?'
        summary = happy_bp.report.getSummaryForQuestion(question)
        average = summary['average']
        min_report = happy_bp.report.getQuestionMin(question)
        max_report = happy_bp.report.getQuestionMax(question)
        return render_template('happiness.html',
                               average=average,
                               max=max_report[0],
                               best_day=max_report[1],
                               min=min_report[0],
                               worst_day=min_report[1])
