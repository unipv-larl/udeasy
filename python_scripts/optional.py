import itertools


def get_core_nodes(features):
    core = {}
    for n in features:
        if not features[n]['optional']:
            core[n] = features[n]
            core[n].pop('optional', None)
    return core


def get_optional_nodes(features):
    optional = {}
    for n in features:
        if features[n]['optional']:
            optional[n] = features[n]
            optional[n].pop('optional', None)
    return optional
