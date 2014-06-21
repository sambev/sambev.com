import json
import operator
from flask import Blueprint, request, Response, render_template
from app.api.classes.reports import ReportsAPI

context_bp = Blueprint('context_bp', __name__,
                   template_folder='templates')


@context_bp.record
def set_up(state):
    context_bp.api = ReportsAPI('static/data/reporter-export.json')


@context_bp.route('/context/<answer>', methods=['GET'])
def get_answer(answer):
    """Get the context for the given answer"""
    if request.method == 'GET':
        context = context_bp.api.getContext(answer)
        for question in context.questions:
            sorted_answers = sorted(
                context.questions[question].iteritems(),
                key=operator.itemgetter(1),
                reverse=True
            )
            context.questions[question] = sorted_answers
        return render_template('context.html', context=context)
