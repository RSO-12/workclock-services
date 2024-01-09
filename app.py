import sys
import logging
import time
from flask import Flask
from flasgger import Swagger
from core.models import db
from core.config import *
from core.util import before_request, after_request, handle_error
from services.auth import auth_bp
from services.reports import reports_bp
from services.health import health_bp
from services.metrics import metrics_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URI}/{DB_NAME}'
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(health_bp)
app.register_blueprint(metrics_bp)

app.before_request(before_request)
app.after_request(after_request)
app.errorhandler(Exception)(handle_error)

swagger = Swagger(app)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
    #with app.app_context():
    #    db.create_all()
