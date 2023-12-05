import os
import sys
import logging
from flask import Flask, jsonify
from flasgger import Swagger
from core.models import db
from services.auth import auth_bp
from services.reports import reports_bp
from services.health import health_bp
from services.metrics import metrics_bp

DB_URI = os.environ.get('DB_URI', 'localhost:8432')
DB_USER = os.environ.get('DB_USER', 'dbuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URI}/workclock-db'
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(health_bp)
app.register_blueprint(metrics_bp)

swagger = Swagger(app)
db.init_app(app)

log_level = logging.DEBUG if app.debug else logging.INFO
logging.basicConfig(level=log_level, stream=sys.stdout)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
    #with app.app_context():
    #    db.create_all()
