from copy_cat.constants import IMPOSSIBLE_HUGE_LENGTH
from copy_cat.utils import find_dictionary


class LengthValidator:
    def __init__(self):
        self.errors = []

    def validate(self, design_object, test_data_object):
        self.validate_length(design_object, test_data_object)

    def validate_length(self, design_object, test_data_object):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        if int(restriction_obj.get('maxLength', IMPOSSIBLE_HUGE_LENGTH)) < int(test_data_object.get('length')):
            error_message = str(f'Given data: \'{test_data_object.get("text")}\' with length ' +
                                str(test_data_object.get('length'))) + ' is bigger then max length of the element: ' + \
                            design_object.get('attributes', [])[0].get('maxLength', IMPOSSIBLE_HUGE_LENGTH)
            self.errors.append({
                "fieldName": test_data_object['name'],
                "fieldPath": design_object['location'],
                "xpath": test_data_object["location"],
                "error": error_message,
            })
