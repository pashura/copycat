from copy_cat.models.error import Error
from copy_cat.utils import get_test_data_object


class RequirementsValidator:
    def __init__(self):
        self.errors = []

    def validate(self, schema, test_data):
        self._validate_requirements(schema, test_data)
        return self.errors

    def _validate_requirements(self, schema, test_data):
        for child in schema['children']:
            if child.get('visible') and child.get('minOccurs') == '1' and not child.get('children'):
                if not get_test_data_object(test_data, child.get('location')):
                    # TODO: Fix error message to be similar to web xd
                    error_message = f"Missing mandatory {child['name']} in {schema['name']} record"
                    self.errors.append(Error(fieldName="",
                                             fieldPath=child['location'],
                                             xpath="",
                                             error=error_message))

            self._validate_requirements(child, test_data)
