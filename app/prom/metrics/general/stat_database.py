from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric


NUMBACKENDS = '''numbackends'''
XACT_COMMIT = '''xact_commit'''
XACT_ROLLBACK = '''xact_rollback'''
BLKS_READ = '''blks_read'''
BLKS_HIT = '''blks_hit'''
TUP_RETURNED = '''tup_returned'''
TUP_FETCHED = '''tup_fetched'''
TUP_INSERTED = '''tup_inserted'''
TUP_UPDATED = '''tup_updated'''
TUP_DELETED = '''tup_deleted'''
CONFLICTS = '''conflicts'''
TEMP_FILES = '''temp_files'''
TEMP_BYTES = '''temp_bytes'''
DEADLOCKS = '''deadlocks'''
BLK_READ_TIME = '''blk_read_time'''
BLK_WRITE_TIME = '''blk_write_time'''
STATS_RESET = '''last_stats_reset_min'''

NAME = '''name'''


class StatDatabase(AbstractMetric):

    def __init__(self, registry, dbVersion):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'postgresql_stat_database'
            , 'Database-wide statistics'
            , labelnames=['database', 'type']
            , registry=registry)

        self.query = ('''
            SELECT
             datname AS %s
             , numbackends AS %s
             , xact_commit AS %s
             , xact_rollback AS %s
             , blks_read AS %s
             , blks_hit AS %s
             , tup_returned AS %s
             , tup_fetched AS %s
             , tup_inserted AS %s
             , tup_updated AS %s
             , tup_deleted AS %s
             , conflicts AS %s
             , temp_files AS %s
             , temp_bytes AS %s
             , deadlocks AS %s
             , blk_read_time AS %s
             , blk_write_time AS %s
             , (DATE_PART('day', current_timestamp - stats_reset) * 24 +
                DATE_PART('hour', current_timestamp - stats_reset)) * 60 +
                DATE_PART('minute', current_timestamp - stats_reset) AS %s
            FROM pg_stat_database
        ''' % (NAME, NUMBACKENDS, XACT_COMMIT, XACT_ROLLBACK, BLKS_READ, BLKS_HIT, TUP_RETURNED, TUP_FETCHED
               , TUP_INSERTED, TUP_UPDATED, TUP_DELETED, CONFLICTS, TEMP_FILES, TEMP_BYTES, DEADLOCKS, BLK_READ_TIME
               , BLK_WRITE_TIME, STATS_RESET))

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self._set_metric(row, NUMBACKENDS)
            self._set_metric(row, XACT_COMMIT)
            self._set_metric(row, BLKS_READ)
            self._set_metric(row, BLKS_HIT)
            self._set_metric(row, TUP_RETURNED)
            self._set_metric(row, TUP_FETCHED)
            self._set_metric(row, TUP_INSERTED)
            self._set_metric(row, TUP_UPDATED)
            self._set_metric(row, TUP_DELETED)
            self._set_metric(row, CONFLICTS)
            self._set_metric(row, TEMP_FILES)
            self._set_metric(row, TEMP_BYTES)
            self._set_metric(row, DEADLOCKS)
            self._set_metric(row, BLK_READ_TIME)
            self._set_metric(row, BLK_WRITE_TIME)
            if row[STATS_RESET] is not None:
                self._set_metric(row, STATS_RESET)

    def _set_metric(self, row, stall_type):
        self.metric \
            .labels(database=row[NAME], type=stall_type) \
            .set(row[stall_type])
