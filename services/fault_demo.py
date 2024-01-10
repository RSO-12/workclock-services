from flask import Blueprint, jsonify
from circuitbreaker import circuit
from core.logger import logger
from core.util import handle_service_unavailable
import random
import time

fault_demo_bp = Blueprint('faults', __name__, url_prefix='/v1/fault/')
GOAL_NUM = 15


class UnluckyException(Exception):
    pass


@fault_demo_bp.route('/demo', methods=['GET'])
def get_demo():
    time.sleep(3)
    num = random.randint(5, 10)
    logger.info(f'Guessed {num}')
    if num != GOAL_NUM:
        logger.error(f'Failed to retrieve correct number - got {num} :/')
        raise UnluckyException('Jup wrong number!')

    return jsonify({'Guessed': True})


@fault_demo_bp.route('/demo-circuit', methods=['GET'])
@circuit(failure_threshold=2, expected_exception=UnluckyException,
         recovery_timeout=60, fallback_function=handle_service_unavailable)
def get_demo_with_circuit():
    time.sleep(3)
    num = random.randint(5, 10)
    logger.info(f'Guessed {num}')
    if num != 7:
        logger.error(f'Failed to retrieve correct number - got {num} :/')
        raise UnluckyException('Jup wrong number!')

    return jsonify({'Guessed': True})
