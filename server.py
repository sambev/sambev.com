from flask import Flask, request, Response, render_template
from werkzeug.contrib.fixers import ProxyFix
from app.blueprints.main import main
from app.blueprints.reports import reports_bp
from app.blueprints.sleep import sleep_bp
from config.jinjacfg import setUpJinjaEnv
from config.settings import SETTINGS


app = Flask(__name__)
setUpJinjaEnv(app)
app.config.update(SETTINGS['dev'])

app.register_blueprint(main)
app.register_blueprint(reports_bp)
app.register_blueprint(sleep_bp)

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run()
