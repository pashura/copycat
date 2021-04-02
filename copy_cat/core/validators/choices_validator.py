from copy_cat.core.validators.abstract_validator import AbstractValidator
from copy_cat.enums.error_type import ErrorType
from copy_cat.models.design import DesignObject
from copy_cat.models.error import Error
from copy_cat.models.test_data import DataObject


class ChoicesValidator(AbstractValidator):
    def validate(
        self, design_object: DesignObject, test_data_object: DataObject
    ) -> None:
        self._validate_choices(design_object, test_data_object)

    def _validate_choices(
        self, design_object: DesignObject, test_data_object: DataObject
    ) -> None:
        if not design_object.restriction:
            return
        if design_object.restriction.display_name == "StringSet":
            qualifiers = [i.strip() for i in design_object.qualifiers.split(",")]
            if (
                test_data_object.value not in qualifiers
                and not design_object.restriction.drop_extra_records
            ):
                # TODO: Fix error message to be similar to web xd
                error_message = (
                    f"Qualifier {test_data_object.value} is not valid. "
                    f"Possible choices -> {qualifiers}"
                )
                self.errors_container.append(
                    Error(
                        fieldName=test_data_object.name,
                        designPath=design_object.location,
                        xpath=test_data_object.location,
                        errorMessage=error_message,
                        errorType=ErrorType.CHOICES,
                    )
                )
