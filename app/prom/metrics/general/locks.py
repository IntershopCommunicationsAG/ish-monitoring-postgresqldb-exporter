from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

COUNT = '''count'''
MODE = '''mode'''
NAME = '''database'''


class Locks(AbstractMetric):

    def __init__(self, registry, app):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'postgresql_lock'
            , ''
            , labelnames=['database', 'mode']
            , registry=registry)

        self.query = '''
            SELECT
             pg_database.datname AS %s
             , tmp.mode AS %s
             , COALESCE(count, 0) as %s
            FROM
                (
                  VALUES ('accesssharelock'),
                         ('rowsharelock'),
                         ('rowexclusivelock'),
                         ('shareupdateexclusivelock'),
                         ('sharelock'),
                         ('sharerowexclusivelock'),
                         ('exclusivelock'),
                         ('accessexclusivelock')
                ) AS tmp(mode) CROSS JOIN pg_database
            LEFT JOIN
              (SELECT database, lower(mode) AS mode,count(*) AS count
              FROM pg_locks WHERE database IS NOT NULL
              GROUP BY database, lower(mode)
            ) AS tmp2
            ON tmp.mode=tmp2.mode and pg_database.oid = tmp2.database ORDER BY 1
        ''' % (NAME, MODE, COUNT)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(database=row[NAME], mode=row[MODE]) \
                .set(row[COUNT])

