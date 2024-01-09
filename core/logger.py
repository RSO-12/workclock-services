import logging
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://elasticsearch:9200'])

class ElasticsearchHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        es.index(index='flask_logs', body={'message': log_entry})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = ElasticsearchHandler()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(stream_handler)
