from flask import Blueprint, request, render_template

main = Blueprint('main', __name__,
                 template_folder='templates')

# TODO Uncomment and configure this to give this blueprint a handle to the db
# @main.record
# def getDB(state):
#     client = MongoClient(state.app.config['DB_URI'])
#     main.db = client[state.app.config['DB_NAME']]

@main.route('/', methods=['GET'])
def index():
    """ Render the landing page """
    if request.method == 'GET':
        return render_template('index.html')