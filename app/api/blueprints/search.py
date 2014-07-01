import json
import operator
from flask import Blueprint, request, Response, render_template
from app.api.classes.reports import ReportsAPI
from app.api.classes.report_summary import ReportSummary

search_bp = Blueprint('search_bp', __name__,
                   template_folder='templates')

@search_bp.record
def set_up(state):
    search_bp.api = ReportsAPI('static/data/reporter-export.json')
    search_bp.summary = ReportSummary('static/data/report-summary.json')


@search_bp.route('/search/', methods=['GET'])
def who_page():
    if request.method == 'GET':
        return render_template('search.html')


@search_bp.route('/search/<name>/', methods=['GET'])
def get_name(name):
    if request.method == 'GET':
        context = search_bp.api.getContext(name)
        if context:
            return Response(json.dumps(context.to_json()))
        else:
            return Response(status=404)
