import pandas as pd
import stats_func


def node_to_conllu(node):
    """
    This function takes a node as argument and returns a string corresponding to the token in the conllu format
    :param node: the node
    :return: the string in the conllu format
    """
    return f'{node._ord}\t{node.form}\t{node.lemma}\t{node.upos}\t{node.xpos}\t{str(node.feats)}' \
           f'\t{node._parent._ord}\t{node.deprel}\t{node._raw_deps}\t{str(node.misc)}'


def get_metadata(sent):
    """
    This function takes a sentence as argument and returns the string containing the metadata
    :param sent: the sentence
    :return: the string containing the metadata (text and sent_id)
    """
    root = sent.get_tree()
    return f'# text = {root.get_sentence()}\n' \
           f'# sent_id = {root._sent_id}\n'


def sent_to_conllu(sent):
    """
    This function takes a sentence as argument and returns a string corresponding to the sentence in the conllu format
    :param sent: the sentence
    :return: the string
    """
    root = sent.get_tree()
    nodes = root.descendants()
    string = get_metadata(sent)
    for node in nodes:
        string += f'{node_to_conllu(node)}\n'
    return string


def str_results(results, conllu=True):
    """
    This function takes as argument the list containing the results and returns them in a string
    :param results: the list containig the results
    :param conllu: if True, returns the matched tokens in conllu format, otherwise it prints only the word-form
    :return: the string
    """
    string = ''
    for res in results:
        for node in res:
            if conllu:
                string += f'{node}: {node_to_conllu(res[node])}\n'
            else:
                string += f'{node}: {res[node].form}\n'
        string += '\n'
    return string


def res2csv(results, fields, path):
    """
    This function takes as arguments the list containing the results, the dict containing the fields to export in the csv and the path where to export the csv file
    """
    rows = []
    nodes = [n for n in fields if n != 'sent']
    for res in results:
        row = {}
        sent_info = stats_func.node2sent_info(res[list(res.keys())[0]])
        for f in fields['sent']:
            row[f] = sent_info[f]
        for n in nodes:
            if n in res:
                node_in_res = res[n]
            else:
                node_in_res = None
            for f in fields[n]:
                if node_in_res:
                    attr = stats_func.get_conllu_attr(node_in_res, f)
                else:
                    attr = None
                row[f'{n}_{f}'] = attr
        rows.append(row)
    df = pd.DataFrame.from_records(rows)
    df.to_csv(path, index=False)


def res2str(res_dict):
    """
    This function turns a results dict into a string
    """
    str = ''
    for k in res_dict:
        str += res_dict[k].form + ' '
    return str
