import itertools
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def get_core_queries(features):
    """ 
    from the features dict select only those elements that are non optionals
    """
    core_q = {}
    for n in features:
        if not features[n]['optional']:
            core_q[n] = features[n].copy()
            # remove the optional key from the dict
            core_q[n].pop('optional', None)
    return core_q


def get_optional_queries(features):
    """ 
    from the features dict select only those elements that are optionals
    """
    optional = {}
    for n in features:
        if features[n]['optional']:
            optional[n] = features[n].copy()
            # remove the optional key from the dict
            optional[n].pop('optional', None)
    return optional


def adapt_condition_list(features, condition_list):
    """
    this function takes the list of features and adapt the list of conditions to include only those that involve the nodes in the features list
    """
    adapted = []
    for c in condition_list:
        if c['node1'] in features and c['node2'] in features:
            adapted.append(c)
    return adapted


def get_queries_list(core_q, optional):
    """
    from the set of core nodes (non optional) and the set of optional nodes, this function creates all the sets of possible combinations
    the core nodes will be present in all the combinations
    """
    qlist = []
    for i in range(1, len(optional) + 1):
        for c in itertools.combinations(optional, i):
            q = core_q.copy()
            for n in c:
                q[n] = optional[n]
            qlist.append(q)
    return sorted(qlist, key=len, reverse=True)


def remove_queries_from_list(queries_list, focus_query):
    """ 
    this function removes the queries that involves a subset of the nodes there are include in the focus query.
    This is made to avoid to include in the results a pattern that includes optional nodes and a subset of the same pattern.
    """ 
    cleaned = []
    for query in queries_list:
        remove = True
        for node in query:
            if node not in focus_query.keys():
                remove = False
        if not remove:
            cleaned.append(query)
    return cleaned


def check_core(core, results_optional):
    """
    This function check that the results of a given query that includes optional nodes, include a core from which that set of results has been generated
    """
    cleaned = []
    for res in results_optional:
        append = True
        for node in core:
            if core[node] != res[node]:
                append = False
        if append:
            cleaned.append(res)
    return cleaned
