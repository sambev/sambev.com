import json
from flask import Blueprint, request, render_template, Response
from app.services.report_api import ReportService


main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route('/', methods=['GET'])
@main.route('/numbers', methods=['GET'])
def numbers():
    return render_template('numbers.html', active='numbers')


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html', active='about')


@main.route('/reports/dates/<string:date>', methods=['GET'])
def view_date(date):
    return render_template('dates.html')
