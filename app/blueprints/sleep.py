import json
from flask import Blueprint, request, Response, render_template
from app.services.sleepapp import SleepAppService

sleep_bp = Blueprint('sleep_bp', __name__, template_folder='templates')

@sleep_bp.record
def init_sleep(state):
    sleep_bp.service = SleepAppService()

@sleep_bp.route('/sleep/summary/', methods=['GET'])
def get_all_quality():
    quality = sleep_bp.service.get_quality_summary()

    return Response(json.dumps(quality))
