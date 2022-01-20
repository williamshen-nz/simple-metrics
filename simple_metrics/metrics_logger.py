import json
import logging
from datetime import datetime
from json import JSONEncoder
from typing import List, Optional

from simple_metrics.metrics import Metric

_log = logging.getLogger(__name__)


class _MetricsEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Metric):
            return o.get_metrics_dict()
        elif isinstance(o, datetime):
            return str(o)
        else:
            super(_MetricsEncoder, self).default(o)


def _generate_metrics_file_name() -> str:
    datetime_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"metrics-{datetime_str}.json"


class MetricsLogger(object):
    """
    Stores metrics
    """

    def __init__(self):
        self.metrics: List[Metric] = []

    def clear(self):
        """Remove all metrics from the Metrics Logger"""
        self.metrics = []

    def add_metric(self, metric: Metric):
        self.metrics.append(metric)

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.metrics, cls=_MetricsEncoder, **kwargs)

    def write_json(self, file_path: Optional[str] = None, **json_kwargs):
        """
        Save metrics to a file as a JSON

        Parameters
        ----------
        file_path: Optional[str], path of the file to save to, if None provided then one
            will be automatically generated based off the current time
        json_kwargs: any parameters to pass to json.dump

        Returns
        -------
        str, path to the JSON metrics file
        """
        if not file_path:
            file_path = _generate_metrics_file_name()

        json.dump(
            self.metrics,
            open(file_path, "w"),
            cls=_MetricsEncoder,
            **json_kwargs,
        )
        _log.info("Dumped MetricsLogger metrics to {file_path}")
        return file_path


# Global metrics logger
metrics_logger = MetricsLogger()
