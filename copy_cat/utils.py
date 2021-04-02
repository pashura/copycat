import re

from copy_cat.common.constants import XPATH_GROUPS_REGEX, XPATH_REP_REGEX


def find_dictionary(lst, key, value):
    return next((dic for dic in (lst or []) if dic.get(key) == value), None)


def get_test_data_object(test_data, location):
    return next(
        (i for i in test_data if get_path_from_location(i.location) == location), None
    )


def get_path_from_location(location):
    return re.sub(XPATH_REP_REGEX, "", location.removeprefix("/"))


# TODO: Refactor -> pay attention on big number of places it used
def get_reps_and_location(location):
    reps = []
    new_paths = []
    for path in location.split("/"):
        if bool(re.search(XPATH_REP_REGEX, path)):
            groups = re.match(XPATH_GROUPS_REGEX, path).groups()
            reps.append({"rep_name": groups[0], "rep_number": groups[1]})
            new_paths.append(groups[0])
        else:
            new_paths.append(path)
    return "/".join(new_paths), reps
