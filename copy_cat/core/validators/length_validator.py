from copy_cat.common.constants import IMPOSSIBLY_HUGE_LENGTH
from copy_cat.core.validators.abstract_validator import AbstractValidator
from copy_cat.enums.error_type import ErrorType
from copy_cat.models.error import Error
from copy_cat.utils import find_dictionary


class LengthValidator(AbstractValidator):
    ihl = IMPOSSIBLY_HUGE_LENGTH

    def validate(self, design_object, test_data_object):
        self.validate_length(design_object, test_data_object)

    def validate_length(self, design_object, test_data_object):
        restriction_obj = find_dictionary(design_object.get("attributes"), "elementType", "restriction") or {}
        max_length = restriction_obj.get('maxLength') or self.ihl
        if test_data_object.length and int(max_length) < int(test_data_object.length or self.ihl):
            # TODO: Fix error message to be similar to web xd
            expected_length = design_object.get('attributes', [])[0].get('maxLength')
            error_message = f"Given data: '{test_data_object.value}' with length {test_data_object.length} " \
                            f"is bigger then max length of the element - " + expected_length

            # TODO: Separate field length and group length validator
            self.errors_container.append(
                Error(
                    fieldName=test_data_object.name,
                    designPath=design_object['location'],
                    xpath=test_data_object.location,
                    errorMessage=error_message,
                    errorType=ErrorType.FIELD_LENGTH
                )
            )
