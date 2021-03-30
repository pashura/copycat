import re

from copy_cat.common.constants import XPATH_GROUPS_REGEX, XPATH_REP_REGEX


def traverse_path_in_schema_object(schema_object: dict, path_to_traverse: str) -> dict or None:
    current_object = schema_object
    if path_to_traverse:
        for n, element in enumerate(path_to_traverse.split("/")):
            current_object = find_child_schema_object(current_object, element)
            if not current_object:
                break
        if current_object:
            return current_object


def find_child_schema_object(parent, name):
    for child in parent.get('children', []):
        if get_schema_object_name(child) == name:
            return child


def get_schema_object_name(schema_object):
    if (name := schema_object.get("name")) and schema_object.get("suffix"):
        name += "-" + schema_object["suffix"]
    return name


def find_dictionary(lst, key, value):
    return next((dic for dic in (lst or []) if dic.get(key) == value), None)


def get_test_data_object(test_data, location):
    return next((i for i in test_data if get_path_from_location(i.location) == location), None)


def get_path_from_location(location):
    return re.sub(XPATH_REP_REGEX, '', location.removeprefix("/"))


def get_reps_and_location(location):
    reps = []
    new_paths = []
    paths = location.split('/')
    for path in paths:
        if bool(re.search(XPATH_REP_REGEX, path)):
            groups = re.match(XPATH_GROUPS_REGEX, path).groups()
            reps.append({
                "rep_name": groups[0],
                "rep_number": groups[1]
            })
            new_paths.append(groups[0])
        else:
            new_paths.append(path)
    return '/'.join(new_paths), reps
