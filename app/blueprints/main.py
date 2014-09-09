import json
from flask import Blueprint, request, render_template, Response
from app.services.report_api import ReportService


main = Blueprint('main', __name__,
                 template_folder='templates')

@main.record
def set_up(state):
    pass


@main.route('/', methods=['GET'])
def index():
    """ Render the landing page """
    if request.method == 'GET':
        return render_template('index.html', active='home')


@main.route('/about', methods=['GET'])
def about():
    if request.method == 'GET':
        return render_template('about.html', active='about')
