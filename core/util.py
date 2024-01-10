from prometheus_client import Counter, Histogram, Summary
from flask import request, jsonify
from core.logger import logger
from datetime import datetime
import time
import requests
import random

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


def handle_service_unavailable():
    logger.error("Service currently not available")
    return jsonify({'error': 'Service currently not available'}), 503


def generate_random_pass():
    url = 'https://gist.githubusercontent.com/borlaym/585e2e09dd6abd9b0d0a/raw/6e46db8f5c27cb18fd1dfa50c7c921a0fbacbad0/animals.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        selected_strings = random.sample(data, 3)
        joined_string = ''.join(selected_strings).replace(" ", "")
        return joined_string
    else:
        return "super_safe_password_placeholder"


def get_first_day_of_month():
    current_date = datetime.now()
    return current_date.replace(year=2020, day=1, hour=0,
                                minute=0, second=0, microsecond=0)

