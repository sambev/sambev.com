import json
from flask import Blueprint, request, render_template, Response
from app.services.report_api import ReportService


main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route('/', methods=['GET'])
@main.route('/numbers', methods=['GET'])
def numbers():
    if request.method == 'GET':
        return render_template('numbers.html', active='numbers')

@main.route('/tokens', methods=['GET'])
def tokens():
    if request.method == 'GET':
        return render_template('tokens.html', active='tokens')

@main.route('/about', methods=['GET'])
def about():
    if request.method == 'GET':
        return render_template('about.html', active='about')
