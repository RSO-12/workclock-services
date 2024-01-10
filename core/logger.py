import logging
from elasticsearch import Elasticsearch
from core.config import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# add elasticsearch logging for PROD
if not IS_DEV:
    es = Elasticsearch(['http://elasticsearch:9200'])
    
    class ElasticsearchHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            es.index(index='flask_logs', body={'message': log_entry})
    
    es_handler = ElasticsearchHandler()
    logger.addHandler(es_handler)
