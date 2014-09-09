import json
from flask import Blueprint, request, Response, render_template
from app.services.report_api import ReportService

reports_bp = Blueprint('reports_bp', __name__, template_folder='templates')

@reports_bp.route('/reports', methods=['GET'])
def reportPage():
    if request.method == 'GET':
        return render_template('reports.html')

@reports_bp.route('/locations/<string:question>/<string:answer>', methods=['GET'])
def locationAPI(question, answer):
    if request.method == 'GET':
        rs = ReportService()
        reports = rs.getLocationReports(question, answer)
        return Response(json.dumps(reports))

@reports_bp.route('/tokens/<string:question>/<string:token>', methods=['GET'])
def tokenAPI(question, token):
    if request.method == 'GET':
        rs = ReportService()
        reports = rs.getReportsByToken(question, token)
        return Response(json.dumps(reports))

@reports_bp.route('/numeric/<string:question>/<string:answer>', methods=['GET'])
def numericAPI(question, answer):
    if request.method == 'GET':
        rs = ReportService()
        reports = rs.getNumericReports(question, answer)
        return Response(json.dumps(reports))

@reports_bp.route('/answered/<string:question>/<string:answer>', methods=['GET'])
def answeredAPI(question, answer):
    if request.method == 'GET':
        rs = ReportService()
        reports = rs.getAnsweredOptions(question, answer)
        return Response(json.dumps(reports))

@reports_bp.route('/geojson/', methods=['GET'])
@reports_bp.route('/geojson/<string:question>/<string:answer>', methods=['GET'])
def getGeoJSON(question=None, answer=None):
    if request.method == 'GET':
        rs = ReportService()
        geojson = rs.getGeoJSONData(question, answer)
        return Response(json.dumps(geojson))
