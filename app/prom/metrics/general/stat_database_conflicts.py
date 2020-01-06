from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

CONFL_TABLESPACE = '''confl_tablespace'''
CONFL_LOCK = '''confl_lock'''
CONFL_SNAPSHOT = '''confl_snapshot'''
CONFL_BUFFERPIN = '''confl_bufferpin'''
CONFL_DEADLOCK = '''confl_deadlock'''

NAME = '''name'''


class StatDatabaseConflicts(AbstractMetric):

    def __init__(self, registry, dbVersion):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'postgresql_stat_database_conflicts'
            , 'Database-wide statistics about query cancels occurring due to conflicts with recovery on standby servers.'
            , labelnames=['database', 'type']
            , registry=registry)

        self.query = ('''
            SELECT
             datname AS %s
             , confl_tablespace AS %s
             , confl_lock AS %s
             , confl_snapshot AS %s
             , confl_bufferpin AS %s
             , confl_deadlock AS %s
            FROM pg_stat_database_conflicts
        ''' % (NAME, CONFL_TABLESPACE, CONFL_LOCK, CONFL_SNAPSHOT
               , CONFL_BUFFERPIN, CONFL_DEADLOCK))

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self._set_metric(row, CONFL_TABLESPACE)
            self._set_metric(row, CONFL_LOCK)
            self._set_metric(row, CONFL_SNAPSHOT)
            self._set_metric(row, CONFL_BUFFERPIN)
            self._set_metric(row, CONFL_DEADLOCK)

    def _set_metric(self, row, stall_type):
        self.metric \
            .labels(database=row[NAME], type=stall_type) \
            .set(row[stall_type])
