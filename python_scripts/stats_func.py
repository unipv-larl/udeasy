from tabulate import tabulate


def get_conllu_attr(node, attr):
    if hasattr(node, attr):
        return getattr(node, attr)
    elif attr in node.feats:
        return node.feats[attr]
    elif attr in node.misc:
        return node.misc[attr]
    else:
        return None


def wo(results: list, stat: dict):
    """
    This function returns a table with the information about the word order of two nodes in the results
    """
    n1_first = 0
    n2_first = 0
    for r in results:
        if r[stat['node1']]._ord < r[stat['node2']]._ord:
            n1_first += 1
        else:
            n2_first += 1
    table = [['order', 'count', 'frequency'],
             [f"{stat['node1']}-{stat['node2']}", n1_first, n1_first / (n1_first + n2_first)],
             [f"{stat['node2']}-{stat['node1']}", n2_first, n2_first / (n1_first + n2_first)]]
    return tabulate(table, headers="firstrow")


def dist(results: list, stat: dict):
    """
    This function returns a dictionary whose elements are:
    - a table with the information about the distribution of the distances between two nodes in the results
    - the average distance between the two nodes
    """
    distances = []
    for r in results:
        distances.append(r[stat['node1']]._ord - r[stat['node2']]._ord)
    table = [[f"distance {stat['node1']}-{stat['node2']}", 'count', 'frequency']]
    absolute = [abs(x) for x in distances]
    for d in sorted(set(distances)):
        table.append([d, distances.count(d), distances.count(d) / len(distances)])
    return {'table': tabulate(table, headers="firstrow"), 'av_dist': sum(absolute) / len(absolute)}


def feat(results: list, stat: list):
    """
    This function returns a table with the information about the distribution of the values of one or more features
    """
    if len(stat) == 1:
        feat_res = []
        s = stat[0]
        for res in results:
            feat_res.append(get_conllu_attr(res[s['node']], s['feat']))
        table = [[s['feat'], 'count', 'frequency']]
        for x in set(feat_res):
            table.append([x, feat_res.count(x), feat_res.count(x) / len(feat_res)])
        return tabulate(table, headers="firstrow")
    elif len(stat) == 2:
        s1 = stat[0]
        feat_res1 = []
        s2 = stat[1]
        feat_res2 = []
        coocc = []
        for res in results:
            feat_res1.append(get_conllu_attr(res[s1['node']], s1['feat']))
            feat_res2.append(get_conllu_attr(res[s2['node']], s2['feat']))
            coocc.append((get_conllu_attr(res[s1['node']], s1['feat']), get_conllu_attr(res[s2['node']], s2['feat'])))
        col_names = [f'{s1["node"]}:{s1["feat"]}/{s2["node"]}:{s2["feat"]}'] + list(set(feat_res2))
        row_names = list(set(feat_res1))
        table = [col_names]
        for r in row_names:
            row = [r]
            for c in col_names[1:]:
                row.append(coocc.count((r, c)))
            table.append(row)
        return tabulate(table, headers="firstrow")
    else:
        coocc = []
        for res in results:
            c = []
            for i in range(len(stat)):
                c.append(get_conllu_attr(res[stat[i]['node']], stat[i]['feat']))
            coocc.append(tuple(c))
        values = list(set(coocc))
        string = f'{stat[0]["node"]}:{stat[0]["feat"]}'
        for i in range(1, len(stat)):
            string += f', {stat[i]["node"]}:{stat[i]["feat"]}'
        table = [[string, 'count', 'frequency']]
        for v in values:
            string = v[0]
            for s in v[1:]:
                string += f', {s}'
            table.append([string, coocc.count(v), coocc.count(v) / len(coocc)])
        return tabulate(table, headers="firstrow")
