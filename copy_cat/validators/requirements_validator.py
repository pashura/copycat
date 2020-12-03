import re

from copy_cat.constants import XPATH_REP_REGEX


class RequirementsValidator:
    def __init__(self):
        self.errors = []

    def validate(self, test_data, schema):
        self._validate_requirements(test_data, schema)
        return self.errors

    def _validate_requirements(self, test_data, schema):
        for child in schema['children']:
            if child.get('visible') is True and child.get('minOccurs') == '1' and not child.get('children'):
                test_data_obj = next((i for i in test_data
                                      if self._get_path_from_location(i["location"]) == child.get('location')), None)
                if not test_data_obj:
                    error_message = f"Missing mandatory {child['name']} in {schema['name']} record"
                    self.errors.append({
                        "fieldName": "",
                        "fieldPath": child['location'],
                        "xpath": "",
                        "error": error_message,
                    })
            self._validate_requirements(test_data, child)

    @staticmethod
    def _get_path_from_location(location):
        return re.sub(XPATH_REP_REGEX, '', location.removeprefix("/"))
