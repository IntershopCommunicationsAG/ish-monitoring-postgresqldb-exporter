from unittest import TestCase
from unittest.mock import MagicMock

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.uptime import Uptime, UPTIME


class TestProcess(TestCase):

    def test_should_collect(self):
        test_data = {UPTIME: 1234}

        app = MagicMock()
        uptime = Uptime(CollectorRegistry(), app)

        uptime.collect(rows=(_ for _ in [test_data]))

        samples = next(iter(uptime.metric.collect())).samples

        self.assertEqual(test_data[UPTIME], next(iter(samples)).value)
