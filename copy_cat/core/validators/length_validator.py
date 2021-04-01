from copy_cat.common.constants import IMPOSSIBLY_HUGE_LENGTH
from copy_cat.core.validators.abstract_validator import AbstractValidator
from copy_cat.enums.error_type import ErrorType
from copy_cat.models.design import DesignObject
from copy_cat.models.error import Error
from copy_cat.models.test_data import DataObject


class LengthValidator(AbstractValidator):

    def validate(self, design_object: DesignObject, test_data_object: DataObject) -> None:
        self._validate_length(design_object, test_data_object)

    def _validate_length(self, design_object: DesignObject, test_data_object: DataObject) -> None:
        if not design_object.restriction:
            return
        max_length = design_object.restriction.max_length or IMPOSSIBLY_HUGE_LENGTH
        test_data_object_length = test_data_object.length or IMPOSSIBLY_HUGE_LENGTH
        if int(max_length) < int(test_data_object_length):
            # TODO: Fix error message to be similar to web xd
            error_message = f"Given data: '{test_data_object.value}' with length {test_data_object.length} " \
                            f"is bigger then max length of the element - " + design_object.restriction.max_length

            # TODO: Separate field length and group length validator
            self.errors_container.append(
                Error(
                    fieldName=test_data_object.name,
                    designPath=design_object.location,
                    xpath=test_data_object.location,
                    errorMessage=error_message,
                    errorType=ErrorType.FIELD_LENGTH
                )
            )
