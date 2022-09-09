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


def adapt_condition_list(features, condition_list):
    adapted = []
    for c in condition_list:
        if c['node1'] in features and c['node2'] in features:
            adapted.append(c)
    return adapted
