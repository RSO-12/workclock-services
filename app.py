import sys
import logging
import time
from flask import Flask, request
from flasgger import Swagger
from core.models import db
from core.config import *
from services.auth import auth_bp
from services.reports import reports_bp
from services.health import health_bp
from services.metrics import metrics_bp
from prometheus_flask_exporter import Counter, Histogram, Summary

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URI}/{DB_NAME}'
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(health_bp)
app.register_blueprint(metrics_bp)

by_path_counter = Counter('by_path_counter', 'Request count by request paths', ['path'])
response_code_counter = Counter('response_code_counter', 'Count of HTTP response codes', ['status_code'])
request_duration_histogram = Histogram('request_duration_seconds', 'Request duration in seconds', ['path'])
request_size_summary = Summary('request_size_bytes', 'Request size in bytes')

@app.before_request
def before_request():
    if '/metrics' not in request.path:
        request.start_time = time.time()

@app.after_request
def after_request(response):
    if '/metrics' not in request.path:
        by_path_counter.labels(request.path).inc()
        response_code_counter.labels(str(response.status_code)).inc()
        duration = time.time() - request.start_time
        request_duration_histogram.labels(request.path).observe(duration)
        if 'Content-Length' in request.headers:
            request_size_summary.observe(int(request.headers['Content-Length']))

    return response

swagger = Swagger(app)
db.init_app(app)

log_level = logging.DEBUG if app.debug else logging.INFO
logging.basicConfig(level=log_level, stream=sys.stdout)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
    #with app.app_context():
    #    db.create_all()
