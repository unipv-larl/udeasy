import udapi.core.node
from tabulate import tabulate
import pandas as pd


def get_conllu_attr(node, attr):
    """
    This function takes as argument a node and an attribute (string) and returns:
    - the attribute if this is one of the conllu fields or subfields (of feats or misc)
    - None otherwise
    """
    if hasattr(node, attr):
        return getattr(node, attr)
    elif attr in node.feats:
        return node.feats[attr]
    elif attr in node.misc:
        return node.misc[attr]
    else:
        return None


def node2sent_info(node: udapi.core.node.Node):
    """
    This function takes as argument a node and returns a dictionary containing the information about the conllu sentence (sent_id and text)
    """
    root = node._root
    return {'sent_id': root.sent_id, 'text': root.get_sentence()}


def reverse_res(res, list_of_nodes):
    """
    This function returns a reversed results dictionary containing only the nodes included in the list passed as argument
    dict = {k1: v1, k2: v2...} --> reversed_dict = {v1: k1, v2: k2...}
    """
    rev = {}
    for r in res:
        if r in list_of_nodes:
            rev[res[r]] = r
    return rev


def get_id(node: udapi.core.node.Node):
    return node._ord


def wo(results: list, stat: dict):
    """
    This function returns a table with the information about the word order of two nodes in the results
    """
    n1_first = 0
    n2_first = 0
    node_missing = 0
    for r in results:
        if stat['node1'] in r and stat['node2'] in r:
            if r[stat['node1']]._ord < r[stat['node2']]._ord:
                n1_first += 1
            else:
                n2_first += 1
        else:
            node_missing += 1
    table = [['order', 'count', 'frequency'],
             [f"{stat['node1']}-{stat['node2']}", n1_first, n1_first / (n1_first + n2_first)],
             [f"{stat['node2']}-{stat['node1']}", n2_first, n2_first / (n1_first + n2_first)],
             [f"results with missing nodes", node_missing, '-']]
    rows = [{'order': f"{stat['node1']}-{stat['node2']}", 'count': n1_first, 'frequency': n1_first / (n1_first + n2_first)},
            {'order': f"{stat['node2']}-{stat['node1']}", 'count': n2_first, 'frequency': n2_first / (n1_first + n2_first)},
            {'order': f"results with missing nodes", 'count': node_missing, 'frequency': None}]
    df = pd.DataFrame.from_records(rows)
    return {'table': tabulate(table, headers="firstrow"), 'df': df}


def wos(results: list, stat: list):
    """
    This function returns a table with the information about the word ordering of of a set of nodes in the results
    """
    table = [["ordering", "count", "frequency"]]
    rows = []
    ords = []
    for res in results:
        rev_res = reverse_res(res, stat)
        ordering = sorted(list(rev_res.keys()), key=get_id)
        t = (rev_res[o] for o in ordering)
        ords.append(', '.join(t))
    for o in set(ords):
        table.append([o, ords.count(o), ords.count(o) / len(ords)])
        rows.append({'ordering': o, 'count': ords.count(o), 'frequency': ords.count(o) / len(ords)})
    df = pd.DataFrame.from_records(rows)
    return {'table': tabulate(table, headers="firstrow"), 'df': df}


def dist(results: list, stat: dict):
    """
    This function returns a dictionary whose elements are:
    - a table with the information about the distribution of the distances between two nodes in the results
    - the average distance between the two nodes
    """
    rows = []
    distances = []
    for r in results:
        if stat['node1'] in r and stat['node2'] in r:
            distances.append(r[stat['node1']]._ord - r[stat['node2']]._ord)
    table = [[f"distance {stat['node1']}-{stat['node2']}", 'count', 'frequency']]
    absolute = [abs(x) for x in distances]
    for d in sorted(set(distances)):
        table.append([d, distances.count(d), distances.count(d) / len(distances)])
        rows.append({f"distance {stat['node1']}-{stat['node2']}": d, 'count': distances.count(d), 'frequency': distances.count(d) / len(distances)})
    df = pd.DataFrame.from_records(rows)
    return {'table': tabulate(table, headers="firstrow"), 'av_dist': sum(absolute) / len(absolute), 'df': df}


def feat(results: list, stat: list):
    """
    This function returns a table with the information about the distribution of the values of one or more features
    """
    rows = []
    if len(stat) == 1:
        feat_res = []
        s = stat[0]
        for res in results:
            if s['node'] in res:
                attr = get_conllu_attr(res[s['node']], s['feat'])
            else:
                attr = 'NotInResults'
            feat_res.append(attr)
        table = [[s['feat'], 'count', 'frequency']]
        for x in set(feat_res):
            table.append([x, feat_res.count(x), feat_res.count(x) / len(feat_res)])
            rows.append({s['feat']: x, 'count': feat_res.count(x), 'frequency': feat_res.count(x) / len(feat_res)})
        df = pd.DataFrame.from_records(rows)
        return {'table': tabulate(table, headers="firstrow"), 'df': df}
    elif len(stat) == 2:
        s1 = stat[0]
        feat_res1 = []
        s2 = stat[1]
        feat_res2 = []
        coocc = []
        for res in results:
            if s1['node'] in res:
                attr1 = get_conllu_attr(res[s1['node']], s1['feat'])
            else:
                attr1 = 'NotInResults'
            if s2['node'] in res:
                attr2 = get_conllu_attr(res[s2['node']], s2['feat'])
            else:
                attr2 = 'NotInResults'
            feat_res1.append(attr1)
            feat_res2.append(attr2)
            coocc.append((attr1, attr2))
        col_names = [f'{s1["node"]}:{s1["feat"]}/{s2["node"]}:{s2["feat"]}'] + list(set(feat_res2))
        row_names = list(set(feat_res1))
        table = [col_names]
        for r in row_names:
            row = [r]
            for c in col_names[1:]:
                row.append(coocc.count((r, c)))
                rows.append({f'{s1["node"]}:{s1["feat"]}-{s2["node"]}:{s2["feat"]}': f"{r}-{c}", 'count': coocc.count((r, c))})
            table.append(row)
        df = pd.DataFrame.from_records(rows)
        return {'table': tabulate(table, headers="firstrow"), 'df': df}
    else:
        coocc = []
        for res in results:
            # count = True
            # for i in range(len(stat)):
            #     if stat[i]['node'] not in res:
            #         count = False
            #         break
            c = []
            for i in range(len(stat)):
                if stat[i]['node'] in res:
                    attr = get_conllu_attr(res[stat[i]['node']], stat[i]['feat'])
                else:
                    attr = 'NotInResults'
                c.append(attr)
            coocc.append(tuple(c))
        values = list(set(coocc))
        string = f'{stat[0]["node"]}:{stat[0]["feat"]}'
        for i in range(1, len(stat)):
            string += f', {stat[i]["node"]}:{stat[i]["feat"]}'
        key = string
        table = [[string, 'count', 'frequency']]
        for v in values:
            string = v[0]
            for s in v[1:]:
                string += f', {s}'
            table.append([string, coocc.count(v), coocc.count(v) / len(coocc)])
            rows.append({key: string, 'count': coocc.count(v), 'frequency': coocc.count(v) / len(coocc)})
        df = pd.DataFrame.from_records(rows)
        return {'table': tabulate(table, headers="firstrow"), 'df': df}
