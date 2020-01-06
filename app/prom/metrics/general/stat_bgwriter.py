from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric


CHECKPOINTS_TIMED = '''checkpoints_timed'''
CHECKPOINTS_REQ = '''checkpoints_req'''
CHECKPOINT_WRITE_TIME = '''checkpoint_write_time'''
CHECKPOINT_SYNC_TIME = '''checkpoint_sync_time'''
BUFFERS_CHECKPOINT = '''buffers_checkpoint'''
BUFFERS_CLEAN = '''buffers_clean'''
MAXWRITTEN_CLEAN = '''maxwritten_clean'''
BUFFERS_BACKEND = '''buffers_backend'''
BUFFERS_BACKEND_FSYNC = '''buffers_backend_fsync'''
BUFFERS_ALLOC = '''buffers_alloc'''
STATS_RESET = '''last_stats_reset_min'''


class BgWriter(AbstractMetric):

    def __init__(self, registry, dbVersion):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'postgresql_stat_bgwriter'
            , 'Statistics about the background writer processes activity'
            , labelnames=['type']
            , registry=registry)

        self.query = ('''
            SELECT
             checkpoints_timed AS %s
             , checkpoints_req AS %s
             , checkpoint_write_time AS %s
             , checkpoint_sync_time AS %s
             , buffers_checkpoint AS %s
             , buffers_clean AS %s
             , maxwritten_clean AS %s
             , buffers_backend AS %s
             , buffers_backend_fsync AS %s
             , buffers_alloc AS %s
             , (DATE_PART('day', current_timestamp - stats_reset) * 24 +
                DATE_PART('hour', current_timestamp - stats_reset)) * 60 +
                DATE_PART('minute', current_timestamp - stats_reset) AS %s
            FROM pg_stat_bgwriter
        ''' % (CHECKPOINTS_TIMED, CHECKPOINTS_REQ, CHECKPOINT_WRITE_TIME, CHECKPOINT_SYNC_TIME
               , BUFFERS_CHECKPOINT, BUFFERS_CLEAN, MAXWRITTEN_CLEAN, BUFFERS_BACKEND, BUFFERS_BACKEND_FSYNC
               , BUFFERS_ALLOC, STATS_RESET))

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self._set_metric(row, CHECKPOINTS_TIMED)
            self._set_metric(row, CHECKPOINTS_REQ)
            self._set_metric(row, CHECKPOINT_WRITE_TIME)
            self._set_metric(row, CHECKPOINT_SYNC_TIME)
            self._set_metric(row, BUFFERS_CHECKPOINT)
            self._set_metric(row, BUFFERS_CLEAN)
            self._set_metric(row, MAXWRITTEN_CLEAN)
            self._set_metric(row, BUFFERS_BACKEND)
            self._set_metric(row, BUFFERS_BACKEND_FSYNC)
            self._set_metric(row, BUFFERS_ALLOC)
            if row[STATS_RESET] is not None:
                self._set_metric(row, STATS_RESET)

    def _set_metric(self, row, stall_type):
        self.metric \
            .labels(type=stall_type) \
            .set(row[stall_type])
