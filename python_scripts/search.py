import io
import itertools
import sys


class QueryResults:
    def __init__(self):
        self.results = []
        self.string = ''
        self.count = {'number of sentences': 0, 'matched sentences': 0, 'matched patterns': 0}

    def process(self, tb, features, relations, positions, show_sent, show_conllu, show_trees):
        """
        This function takes as argument the parameters inserted in the main frame and returns a tuple containing:
            - the matched patterns in a str format
            - a list containing all the matched patterns
            - a dictionary containing some preliminary statistics about the matched patterns
        :param tb: the treebank object
        :param features: the features query
        :param relations: the relations query
        :param positions: the positions query
        :param show_sent: a boolean variable. If True, show the sentence in conllu format along with the results
        :param show_conllu: a boolean variable. If True, it returns the nodes in conllu format otherwise, it returns only
        the word forms
        """
        for sentence in tb:
            self.count['number of sentences'] += 1
            sent_res = sent_results(sentence, features, relations, positions)
            if sent_res:
                self.count['matched sentences'] += 1
                self.count['matched patterns'] += len(sent_res)
                self.results += sent_res
                if show_sent:
                    self.string += sent_to_conllu(sentence) + '\n'
                else:
                    self.string += get_metadata(sentence) + '\n'
                if show_trees:
                    sys.stdout = io.StringIO()
                    sentence.draw(color=None, print_sent_id=False, print_doc_meta=False, print_text=False, indent=2)
                    self.string += sys.stdout.getvalue()
                sys.stdout = sys.__stdout__
                self.string += str_results(sent_res, show_conllu) + '\n\n'


def str2list(s):
    """
    This function converts a string that starts with '[' and ends with ']' into a list. Its elements will be the
    results of the spit of the rest of the string using ',' as separator
    :param s: the string
    :return: the list
    """
    if s[0] == '[' and s[-1] == ']':
        return [x.strip() for x in s[1:-1].split(',')]


def convert(truth_value, change_value):
    if change_value:
        return not truth_value
    else:
        return truth_value


def match_condition(node, c):
    """
    This function takes a node and a conditions_dict and checks whether the node match all the conditions
    :param node: a node
    :param c: the conditions dictionary
    :return: True or False
    """
    for key in c:
        raw_val = c[key]
        if raw_val.startswith('###NOT###'):
            change_value = True
            val = raw_val[len('###NOT###'):]
        else:
            change_value = False
            val = raw_val
        if not key:
            return True
        elif not hasattr(node, key):
            if key not in node.feats and key not in node.misc:
                return convert(False, change_value)
            elif isinstance(str2list(val), list):
                if key in node.feats:
                    if node.feats[key] not in str2list(val):
                        return convert(False, change_value)
                else:
                    if node.misc[key] not in str2list(val):
                        return convert(False, change_value)
            else:
                if key in node.feats:
                    if node.feats[key] != val:
                        return convert(False, change_value)
                else:
                    if node.misc[key] != val:
                        return convert(False, change_value)
        elif isinstance(str2list(val), list):
            if getattr(node, key) not in str2list(val):
                return convert(False, change_value)
        else:
            if getattr(node, key) != val:
                return convert(False, change_value)
    return convert(True, change_value)


def condition_matched(condition, bundle):
    """
    This function checks if a feature condition is matched in a sentence and returns a list containing all the nodes matching
    such condition
    :param condition: the features dictionary
    :param bundle: the sentence
    :return: list of nodes
    """
    list_of_nodes = bundle.get_tree().descendants()
    return [node for node in list_of_nodes if match_condition(node, condition)]


def get_candidates_features(features, bundle):
    node_names = list(features.keys())
    candidates = []
    conditions = [features[n] for n in node_names]
    matched = [condition_matched(c, bundle) for c in conditions]
    for element in [p for p in itertools.product(*matched) if len(set(p)) == len(p)]:
        candidates.append({node_names[i]: element[i] for i in range(len(node_names))})
    return candidates


def match_relation(rel, c):
    """
    This function take a relation dictionary condition and a candidate (a set of nodes) as arguments and tells if the
    candidate meets the condition
    :param rel: the relation dictionary
    :param c: the candidate
    :return: True or False
    """
    if rel['rel'] == 'is parent of':
        if c[rel['node2']]._parent == c[rel['node1']]:
            return True
        else:
            return False
    elif rel['rel'] == 'is ancestor of':
        if c[rel['node2']] in c[rel['node1']].descendants:
            return True
        else:
            return False
    elif rel['rel'] == 'is sibling of':
        if c[rel['node1']]._parent == c[rel['node2']]._parent:
            return True
        else:
            return False
    else:
        return True


def match_relations(rel_list, c):
    """
    This function takes a list of relation conditions and a candidate and tells if the candidate meets all the
    contitions
    :param rel_list: the list of position conditions
    :param c: the candidate
    :return: True or False
    """
    for rel in rel_list:
        if not match_relation(rel, c):
            return False
    return True


def filter_candidates_relations(rel_list, candidates):
    """
    This function takes a list of relation conditions and a list of candidates and filter this list keeping only the
    candidates that meet all the conditions
    :param rel_list: the list of position conditions
    :param candidates: the list cof candidates
    :return: the filtered list
    """
    result = []
    for c in candidates:
        if match_relations(rel_list, c):
            result.append(c)
    return result


def match_position(pos, c):
    """
    This function take a position dictionary condition and a candidate (a set of nodes) as arguments and tells if the
    candidate meets the condition
    :param pos: the position dictionary
    :param c: the candidate
    :return: True or False
    """
    if pos['rel'] == 'precedes':
        if pos['dist']:
            d = int(pos['dist'])
            if pos['by'] == 'by exactly':
                if d == c[pos['node2']].ord - c[pos['node1']].ord:
                    return True
                else:
                    return False
            else:
                if d >= c[pos['node2']].ord - c[pos['node1']].ord:
                    return True
                else:
                    return False
        else:
            if c[pos['node2']] > c[pos['node1']]:
                return True
            else:
                return False
    if pos['rel'] == 'follows':
        if pos['dist']:
            d = int(pos['dist'])
            if pos['by'] == 'by exactly':
                if d == c[pos['node1']].ord - c[pos['node2']].ord:
                    return True
                else:
                    return False
            else:
                if d >= c[pos['node1']].ord - c[pos['node2']].ord:
                    return True
                else:
                    return False
        else:
            if c[pos['node1']] > c[pos['node2']]:
                return True
            else:
                return False
    else:
        return True


def match_positions(pos_list, c):
    """
    This function takes a list of position conditions and a candidate and tells if the candidate meets all the
    contitions
    :param pos_list: the list of position conditions
    :param c: the candidate
    :return: True or False
    """
    for pos in pos_list:
        if not match_position(pos, c):
            return False
    return True


def filter_candidates_positions(pos_list, candidates):
    """
    This function takes a list of position conditions and a list of candidates and filter this list keeping only the
    candidates that meet all the conditions
    :param pos_list: the list of position conditions
    :param candidates: the list cof candidates
    :return: the filtered list
    """
    result = []
    for c in candidates:
        if match_positions(pos_list, c):
            result.append(c)
    return result


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


def sent_results(sentence, features, relations, positions):
    candidates1 = get_candidates_features(features, sentence)
    candidates2 = filter_candidates_relations(relations, candidates1)
    results = filter_candidates_positions(positions, candidates2)
    return results
