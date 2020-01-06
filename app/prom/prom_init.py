"""Initialize prom"""

from prometheus_client.registry import CollectorRegistry

from app.prom.collector import Collector
from app.prom.metrics.abstract_metric import AbstractMetric
from app.prom.database import util as db_util

class PromInitializer:
    """
    Initialize prom that should be used during app creation and shared in flask context(current_app)
    """

    def __init__(self, app):
        self.registry = CollectorRegistry()

        with app.app_context():

            # get db version
            # will be executed once on startup
            if db_util.is_port_open():
                dbVersion = db_util.get_version()

                self.metrics = [
                    obj(self.registry, dbVersion) for obj in AbstractMetric.__subclasses__()
                ]

                assert len(
                    self.metrics) != 0, "At least one metric should be initialized"

                # Prometheus setup
                self.collector = Collector(self.metrics)
