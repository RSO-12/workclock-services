from flask import Flask
from flasgger import Swagger
from core.models import db
from core.config import *
from core.util import before_request, after_request, handle_error
from services.auth import auth_bp
from services.reports import reports_bp
from services.health import health_bp
from services.metrics import metrics_bp
from services.mock import mock_bp
from services.fault_demo import fault_demo_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URI}/{DB_NAME}'
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(health_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(mock_bp)
app.register_blueprint(fault_demo_bp)

app.before_request(before_request)
app.after_request(after_request)
app.errorhandler(Exception)(handle_error)

swagger = Swagger(app)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
