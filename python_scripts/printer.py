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


def res2str(res_dict):
    str = ''
    for k in res_dict:
        str += res_dict[k].form + ' '
    return str
