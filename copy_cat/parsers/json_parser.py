
def flatten(current: dict, result=None):
    if result is None:
        result = []
    if isinstance(current, dict) and current.get('text') is None:
        for key in current:
            flatten(current[key], result)
    elif isinstance(current, list):
        for key in current:
            flatten(key, result)
    elif isinstance(current, dict) and current.get('text') is not None:
        result.append(current)

    return result


def parse(jsn):
    result = []

    result = flatten(jsn, result)

    return result
