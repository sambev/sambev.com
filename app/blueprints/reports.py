import json
from flask import Blueprint, request, Response, render_template
from app.services.report_api import ReportService
from app.services.sleepapp import SleepAppService

reports_bp = Blueprint('reports_bp', __name__, template_folder='templates')


@reports_bp.record
def init_reports(state):
    reports_bp.service = ReportService()


@reports_bp.route('/reports/people/context/<string:name>', methods=['GET'])
@reports_bp.route('/reports/places/context/<string:name>', methods=['GET'])
@reports_bp.route('/reports/activities/context/<string:name>', methods=['GET'])
def context(name):
    if request.method == 'GET':
        return render_template('tokens.html', active='tokens')


@reports_bp.route('/api/reports', methods=['GET'])
def reportPage():
    if request.method == 'GET':
        reports = reports_bp.service.get_all_reports()

        return Response(json.dumps(reports))


@reports_bp.route('/api/reports/dates', methods=['GET'])
def get_report_dates():
    if request.method == 'GET':
        dates = reports_bp.service.get_report_dates()

        return Response(json.dumps(dates))


@reports_bp.route('/api/reports/dates/<string:date>', methods=['GET'])
def get_reports_for_date(date):
    if request.method == 'GET':
        reports = reports_bp.service.get_reports_for_date(date)

        return Response(json.dumps(reports))


@reports_bp.route('/api/reports/totals', methods=['GET'])
def totals():
    if request.method == 'GET':
        totals = reports_bp.service.get_report_totals()

        return Response(json.dumps(totals))


@reports_bp.route('/api/reports/summary/numeric/<string:question>', methods=['GET'])
def numeric_summary(question=None):
    if request.method == 'GET':
        summary = reports_bp.service.get_numeric_summary(question)

        return Response(json.dumps(summary))


@reports_bp.route('/api/reports/summary/token/<string:question>', methods=['GET'])
def token_summary(question=None):
    if request.method == 'GET':
        summary = reports_bp.service.get_token_summary(question)

        return Response(json.dumps(summary))


@reports_bp.route('/api/reports/summary/location/<string:question>', methods=['GET'])
def location_summary(question=None):
    if request.method == 'GET':
        summary = reports_bp.service.get_location_summary(question)

        return Response(json.dumps(summary))


@reports_bp.route('/api/reports/locations/<string:question>/<string:answer>', methods=['GET'])
def locationAPI(question, answer):
    if request.method == 'GET':
        reports = reports_bp.service.getLocationReports(question, answer)

        return Response(json.dumps(reports))


@reports_bp.route('/api/reports/tokens/<string:question>/<string:token>', methods=['GET'])
def tokenAPI(question, token):
    if request.method == 'GET':
        reports = reports_bp.service.getReportsByToken(question, token)

        return Response(json.dumps(reports))


@reports_bp.route('/api/reports/numeric/<string:question>/', methods=['GET'])
@reports_bp.route('/api/reports/numeric/<string:question>/<string:answer>', methods=['GET'])
def numericAPI(question, answer=None):
    if request.method == 'GET':
        reports = reports_bp.service.getNumericReports(question, answer)

        return Response(json.dumps(reports))


@reports_bp.route('/api/reports/answered/<string:question>/<string:answer>', methods=['GET'])
def answeredAPI(question, answer):
    if request.method == 'GET':
        reports = reports_bp.service.getAnsweredOptions(question, answer)

        return Response(json.dumps(reports))


@reports_bp.route('/api/reports/geojson/', methods=['GET'])
@reports_bp.route('/api/reports/geojson/<string:question>/<string:answer>', methods=['GET'])
def getGeoJSON(question=None, answer=None):
    if request.method == 'GET':
        geojson = reports_bp.service.getGeoJSONData(question, answer)

        return Response(json.dumps(geojson))
