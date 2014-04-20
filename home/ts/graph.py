from datetime import timedelta
from functools import partial
from itertools import groupby

AGGREGATORS = {
    'delta': lambda dps: max(dps) - min(dps),
    'max': max,
    'mean': lambda dps: round(sum(dps) / min(len(dps), 1), 2),
    'min': min,
}


class AggregatedResultSet:

    def __init__(self, group, duration, values):

        self.group = group
        self.duration = duration
        self.values = values

    def aggregate(self):

        aggregates = {}

        for aggregator, f in AGGREGATORS.items():

            aggregates[aggregator] = f([dp.value for dp in self.values])

        return aggregates


def get_method(graph_model):

    if graph_model is None:
        return

    return group_values


def round_datetime(data_point, round_by):
    seconds = (data_point.created_at - data_point.created_at.min).seconds
    rounding = (seconds + round_by / 2) // round_by * round_by
    d = timedelta(0, rounding-seconds, -data_point.created_at.microsecond)
    return data_point.created_at + d


def group_values(values):

    seconds = 60 * 60

    key = partial(round_datetime, round_by=seconds)

    for group, group_values in groupby(values, key=key):

        group_values = list(group_values)

        yield AggregatedResultSet(group=group, duration=seconds,
                                  values=group_values)
