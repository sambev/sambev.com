import json
from flask import Blueprint, request, Response
from app.api.classes.report_summary import ReportSummary

rep_bp = Blueprint('rep_bp', __name__,
                   template_folder='templates')


@rep_bp.record
def set_up(state):
    rep_bp.report = ReportSummary('static/data/report-summary.json')


@rep_bp.route('/reports', methods=['GET'])
def report():
    """ Render the landing page """
    if request.method == 'GET':
        return Response([json.dumps(rep_bp.report.summaries)])


@rep_bp.route('/reports/top_five/<question>', methods=['GET'])
def top_five(question):
    if request.method == 'GET':
        top_five = rep_bp.report.getTopFive(question)
        if top_five:
            return Response(json.dumps(top_five), status=200)
