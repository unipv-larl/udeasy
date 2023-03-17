import yaml


def export_q(data, dest):
    with open(dest, 'w') as file:
        yaml.safe_dump(data, file)


def import_q(path):
    with open(path) as file:
        data = yaml.safe_load(file)
    if valid_imported(data):
        return data


def valid_imported(data) -> bool:
    # checking if the loaded query is a dict
    if isinstance(data, dict):
        # checking if 'features' is present as a key of the query dict
        if 'features' not in data:
            return False
        features = data['features']
        # checking the features and getting the list of nodes
        nodes = valid_features(features)
        if not nodes:
            return False
    else:
        return False


def valid_features(features) -> list:
    """
    This function checks the features dict imported from the yaml file and
    returns the list of nodes names if it is well formed, otherwise it
    returns an empty list

    Arguments:
    features: the features dict

    Returns:
    list: the list of nodes if features is a well formed dict, an empty list
    otherwise
    """
    # checking if features is a dict
    if not isinstance(features, dict):
        return []
    # checking if features is empty
    if not features:
        return []
    nodes = []
    # loop through nodes
    for n in features:
        # check if the node key is a string and if it has a dict as value
        if not isinstance(n, str) or not isinstance(features[n], dict):
            return []
        nodes.append(n)
        # check if the optional key is in the node dict
        if 'optional' not in features[n]:
            return []
    # return the list of nodes
    return nodes


def valid_relations(relations, nodes) -> bool:
    pass


def valid_positions(positions, nodes) -> bool:
    pass


def valid_shows(shows) -> bool:
    pass
