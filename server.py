from flask import Flask, request, Response, render_template
from app.api.blueprints.main import main
from app.api.blueprints.report import rep_bp
from config.jinjacfg import setUpJinjaEnv
from config.settings import SETTINGS


app = Flask(__name__)
setUpJinjaEnv(app)
app.config.update(SETTINGS['dev'])

app.register_blueprint(main)
app.register_blueprint(rep_bp)

if __name__ == "__main__":
    app.run()
