from prometheus_client import Counter, Histogram, Summary
from flask import request, jsonify
from core.logger import logger
import time

by_path_counter = Counter('by_path_counter', 'Request count by request paths', ['path'])
response_code_counter = Counter('response_code_counter', 'Count of HTTP response codes', ['status_code'])
request_duration_histogram = Histogram('request_duration_seconds', 'Request duration in seconds', ['path'])
request_size_summary = Summary('request_size_bytes', 'Request size in bytes')

def before_request():
    if '/metrics' not in request.path:
        request.start_time = time.time()

def after_request(response):
    if '/metrics' not in request.path:
        by_path_counter.labels(request.path).inc()
        response_code_counter.labels(str(response.status_code)).inc()
        duration = time.time() - request.start_time
        request_duration_histogram.labels(request.path).observe(duration)
        if 'Content-Length' in request.headers:
            request_size_summary.observe(int(request.headers['Content-Length']))

    return response

def handle_error(e):
    logger.error(f"An error occurred: {e}")
    return jsonify({'error': 'Something went wrong'}), 500
