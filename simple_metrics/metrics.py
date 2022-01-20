import json
from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Union

from simple_metrics.types import Number


class MetricUnit(Enum):
    Seconds = "seconds"
    Count = "count"


class Metric(ABC):
    def __init__(
        self,
        name: str,
        value: Number,
        unit: MetricUnit,
        timestamp: datetime = None,
        context: Optional[Dict[str, Union[str, Number]]] = None,
    ):
        self.name = name
        self.value = value
        self.unit = unit
        self.timestamp = timestamp if timestamp else datetime.now()
        self.context = context if context else {}

    def get_metrics_dict(self) -> dict:
        return {
            self.name: {
                "value": self.value,
                "unit": self.unit.value,
                "context": self.context,
                "timestamp": self.timestamp,
            }
        }

    def to_json(self) -> str:
        return json.dumps(self.get_metrics_dict())


class TimeMetric(Metric):
    def __init__(
        self,
        name: str,
        value: Number,
        timestamp: datetime = None,
        context: Optional[Dict[str, Union[str, Number]]] = None,
    ):
        super(TimeMetric, self).__init__(
            name, value, MetricUnit.Seconds, timestamp, context
        )


class CountMetric(Metric):
    def __init__(
        self,
        name: str,
        value: Number,
        timestamp: datetime = None,
        context: Optional[Dict[str, Union[str, Number]]] = None,
    ):
        super(CountMetric, self).__init__(
            name, value, MetricUnit.Count, timestamp, context
        )
