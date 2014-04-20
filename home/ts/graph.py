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

    def __init__(self, group, duration, value):

        self.group = group
        self.duration = duration
        self.value = value

    def as_dict(self):
        return {
            'created_at': self.group,
            'value': self.value
        }


def round_datetime(data_point, round_by):
    seconds = (data_point.created_at - data_point.created_at.min).seconds
    rounding = (seconds + round_by / 2) // round_by * round_by
    d = timedelta(0, rounding-seconds, -data_point.created_at.microsecond)
    return data_point.created_at + d


def group_values(values, aggregator_functions):

    seconds = 60 * 60

    key = partial(round_datetime, round_by=seconds)

    results = [[] for _ in aggregator_functions]

    for group, group_values in groupby(values, key=key):

        group_values = list(group_values)

        for i, aggregator_function in enumerate(aggregator_functions):
            f = AGGREGATORS[aggregator_function]
            value = f([dp.value for dp in group_values])

            results[i].append(AggregatedResultSet(group=group,
                              duration=seconds, value=value))

    return results


FUNCTIIONS = {
    'minmax': partial(group_values, aggregator_functions=['min', 'max', ]),
    'delta': partial(group_values, aggregator_functions=['delta', ])
}


def get_method(graph_model):

    if graph_model is None:
        return

    f = FUNCTIIONS.get(graph_model.aggregator)

    return f
