from copy_cat.models.test_data import DataObject
from copy_cat.models.validation_condition import Conditions
from copy_cat.validators.abstract_validator import AbstractValidator
from copy_cat.validators.validation_conditions.errors_generator import ErrorsGenerator
from copy_cat.validators.validation_conditions.utils import get_successful_conditions_count


class AtLeastOneOfValidator(AbstractValidator):
    def validate(self, validations: list, test_data: list[DataObject], location: str):
        for validation in validations:
            if not self._conditions_satisfied(validation.rules[0], test_data, location):
                self.errors_container.append(ErrorsGenerator.generate(validation, location))

    @staticmethod
    def _conditions_satisfied(conditions: Conditions, test_data: list[DataObject], location: str) -> bool:
        count = get_successful_conditions_count(conditions.conditions, test_data, location)
        return bool(count)
