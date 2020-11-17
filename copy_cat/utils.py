def traverse_path_in_schema_object(schema_object: dict, path_to_traverse: str) -> dict:
    current_object = schema_object
    if path_to_traverse:
        for n, element in enumerate(path_to_traverse.split("/")):
            parent_name = current_object.get("name")
            current_object = find_child_schema_object(current_object, element)
            if not current_object:
                print(parent_name, element)
                # raise Exception(parent_name, element)
        if current_object:
            return current_object


def find_child_schema_object(parent, name):
    for child in parent.get('children', []):
        if get_schema_object_name(child) == name:
            return child


def get_schema_object_name(schema_object):
    name = schema_object.get("name")
    if name and schema_object.get("suffix"):
        name += "-" + schema_object["suffix"]
    return name


def find_dictionary(lst, key, value):
    if lst:
        return next((dic for dic in lst if dic.get(key) == value), None)
