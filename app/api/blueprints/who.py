import json
import operator
from flask import Blueprint, request, Response, render_template
from app.api.classes.reports import ReportsAPI
from app.api.classes.report_summary import ReportSummary

who_bp = Blueprint('who_bp', __name__,
                   template_folder='templates')

@who_bp.record
def set_up(state):
    who_bp.api = ReportsAPI('static/data/reporter-export.json')
    who_bp.summary = ReportSummary('static/data/report-summary.json')


@who_bp.route('/who/', methods=['GET'])
def who_endpoint():
    if request.method == 'GET':
        top_five = who_bp.summary.getTopFive('Who are you with?')
        return render_template('who.html', top_five=top_five)
