from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.stat_activity import StatActivity, COUNT, STATE, NAME


class TestStatActivity(TestCase):

    def test_should_collect(self):
        test_data_1 = {NAME: 'grafanadb', STATE: 'idle', COUNT: 300}
        test_data_2 = {NAME: 'grafanadb', STATE: 'busy', COUNT: 3}

        activity = StatActivity(CollectorRegistry(), '9.2.0')

        activity.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(activity.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, COUNT)
        self.assert_sample_metrics(iter_samples, test_data_2, COUNT)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[NAME], sample.labels['database'])
        self.assertEqual(test_data[STATE], sample.labels['state'])
