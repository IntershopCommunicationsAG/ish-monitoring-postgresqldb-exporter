from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

COUNT = '''count'''
STATE = '''state'''
NAME = '''database'''
MAX_TX_DURATION = '''max_tx_duration'''


class StatActivity(AbstractMetric):

    def __init__(self, registry, app):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'postgresql_stat_activity'
            , ''
            , labelnames=['database', 'state']
            , registry=registry)

        with app.app_context():
            if db_util.dbVersionIsGreaterOrEqual('9.2.0'):
                self.query = '''
                    SELECT
                        pg_database.datname AS %s,
                        tmp.state AS %s,
                        COALESCE(count,0) AS %s,
                        COALESCE(max_tx_duration,0) AS %s
                    FROM
                        (
                          VALUES ('active'),
                                   ('idle'),
                                   ('idle in transaction'),
                                   ('idle in transaction (aborted)'),
                                   ('fastpath function call'),
                                   ('disabled')
                        ) AS tmp(state) CROSS JOIN pg_database
                    LEFT JOIN
                    (
                        SELECT
                            datname,
                            state,
                            count(*) AS count,
                            MAX(EXTRACT(EPOCH FROM now() - xact_start))::float AS max_tx_duration
                        FROM pg_stat_activity GROUP BY datname,state) AS tmp2
                        ON tmp.state = tmp2.state AND pg_database.datname = tmp2.datname
                ''' % (NAME, STATE, COUNT, MAX_TX_DURATION)
            else:
                self.query = '''
                    SELECT
                        datname AS %s,
                        'unknown' AS %s,
                        COALESCE(count(*),0) AS %s,
                        COALESCE(MAX(EXTRACT(EPOCH FROM now() - xact_start))::float,0) AS %s
                    FROM pg_stat_activity GROUP BY datname
                ''' % (NAME, STATE, COUNT, MAX_TX_DURATION)
                super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(database=row[NAME], state=row[STATE]) \
                .set(row[COUNT])

