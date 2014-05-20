"""
home.ts.graph
=============

A set of graph aggregation functions that are used to process the results so
we can display them in different ways. For example, rather than showing an
increasing total watts we can show how much was used in the hour.
"""

from datetime import timedelta, datetime
from decimal import Decimal
from collections import defaultdict
from functools import partial
from itertools import groupby

AGGREGATORS = {
    'delta': lambda dps: max(dps) - min(dps),
    'max': max,
    'mean': lambda dps: round(sum(dps) / min(len(dps), 1), 2),
    'min': min,
}


def round_datetime(data_point, round_by):
    created_at = datetime.strptime(data_point[0], "%Y-%m-%dT%H:%M:%S.%f")
    seconds = (created_at - created_at.min).seconds
    rounding = (seconds + round_by / 2) // round_by * round_by
    d = timedelta(0, rounding-seconds, - created_at.microsecond)
    return created_at + d


def group_values(values, aggregator_functions):

    seconds = 60 * 60

    key = partial(round_datetime, round_by=seconds)

    results = defaultdict(list)

    for group, group_values in groupby(values, key=key):

        group_values = list(group_values)

        for i, aggregator_function in enumerate(aggregator_functions):
            f = AGGREGATORS[aggregator_function]
            value = f([Decimal(dp[1]) for dp in group_values])

            results[aggregator_function].append((group, value))

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
