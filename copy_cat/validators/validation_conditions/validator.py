import collections

from copy_cat.models.test_data import DataObject
from copy_cat.models.validation_condition import ValidationCondition
from copy_cat.validators.abstract_validator import AbstractValidator
from copy_cat.validators.validation_conditions import validation_condition_factory
from copy_cat.validators.validation_conditions.exceptions import UnsupportedValidationConditionTypeError


class ValidationConditionsValidator(AbstractValidator):
    def validate(self, design_object: dict, test_data: list[DataObject]):
        self._validate_conditions(design_object, test_data)
        self._validate_children(design_object['children'], test_data)

    def _validate_children(self, children: list, test_data: list[DataObject]):
        for child in children:
            self._validate_conditions(child, test_data)
            self._validate_children(child.get('children', []), test_data)

    def _validate_conditions(self, design_object: dict, test_data: list[DataObject]):
        if (validations := design_object.get('validation', [])) and design_object['visible']:
            for conditions_type, conditions in self._get_grouped_validation_conditions(validations).items():
                try:
                    validator = validation_condition_factory(conditions_type)
                    validator.validate(conditions, test_data, design_object['location'])
                except UnsupportedValidationConditionTypeError:
                    print(f'Conditions {conditions_type} skipped')

    @staticmethod
    def _get_grouped_validation_conditions(validation_conditions: list) -> dict:
        grouped_validation_conditions = collections.defaultdict(list)
        for condition in validation_conditions:
            grouped_validation_conditions[condition['type']].append(ValidationCondition(**condition))
        return grouped_validation_conditions
