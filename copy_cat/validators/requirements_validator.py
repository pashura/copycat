from copy_cat.models.error import Error
from copy_cat.utils import get_test_data_object
from copy_cat.validators.abstract_validator import AbstractValidator


class RequirementsValidator(AbstractValidator):
    def validate(self, design, test_data):
        self._validate_requirements(design, test_data)

    def _validate_requirements(self, design_object, test_data):
        for child in design_object['children']:
            if child.get('visible') and child.get('minOccurs') == '1' and not child.get('children'):
                if not get_test_data_object(test_data, child.get('location')):
                    # TODO: Fix error message to be similar to web xd
                    error_message = f"Missing mandatory {child['name']} in {design_object['name']} record"
                    self.errors_container.append(Error(fieldName="",
                                                       designPath=child['location'],
                                                       xpath="",
                                                       errorMessage=error_message))

            self._validate_requirements(child, test_data)
