from itertools import cycle

from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

UPTIME = '''uptime'''


class Uptime(AbstractMetric):

    def __init__(self, registry, app):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'postgresql_uptime'
            , 'Gauge metric with uptime in days of the Instance.'
            , registry=registry)

        self.query = '''
        select extract(day from date_trunc('day', current_timestamp - pg_postmaster_start_time())) AS %s
        ''' % UPTIME

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        licycle = cycle(rows)
        self.metric.set(next(licycle)[UPTIME])
