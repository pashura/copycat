from copy_cat.models.test_data import DataObject
from copy_cat.models.validation_condition import Conditions
from copy_cat.core.validators.abstract_validator import AbstractValidator
from copy_cat.core.validators.validation_conditions.errors_generator import (
    ErrorsGenerator,
)
from copy_cat.core.validators.validation_conditions.utils import (
    get_successful_conditions_count,
)


class IfThenValidator(AbstractValidator):
    def validate(self, validations: list, test_data: list[DataObject], location: str):
        for validation in validations:
            if self._conditions_satisfied(
                validation.conditions[0], test_data, location
            ):
                if not self._conditions_satisfied(
                    validation.results[0], test_data, location
                ):
                    self.errors_container.append(
                        ErrorsGenerator.generate(validation, location)
                    )

    @staticmethod
    def _conditions_satisfied(
        conditions: Conditions, test_data: list[DataObject], location: str
    ) -> bool:
        conjunction = conditions.conjunction
        conditions = conditions.conditions
        count = get_successful_conditions_count(conditions, test_data, location)
        return (conjunction == "or" and count > 0) or (
            conjunction == "and" and count == len(conditions)
        )
