import logging

from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

UP = '''postgresql_up'''

LOGGER = logging.getLogger(__name__)


class Up(AbstractMetric):

    def __init__(self, registry, app):
        """
        Initialize query and metrics
        """
        self.is_up_metric = True

        self.metric = Gauge('postgresql_up', 'PostgreSQL exporter UP status', registry=registry)

        super().__init__()

    def collect(self, app):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """

        with app.app_context():
            if db_util.is_port_open():
                self.metric.set(1)
                LOGGER.info("PostgreSQLDB is UP")
            else:
                self.metric.set(0)
                LOGGER.info("PostgreSQLDB is DOWN")
