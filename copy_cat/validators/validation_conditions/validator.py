import collections

from copy_cat.models.validation_condition import ValidationCondition
from copy_cat.validators.validation_conditions import validation_condition_factory
from copy_cat.validators.validation_conditions.exceptions import UnsupportedValidationConditionTypeError


class ValidationConditionsValidator:
    def __init__(self):
        self.errors = []

    def validate(self, design_object: dict, test_data: list) -> list:
        self._validate_conditions(design_object, test_data)
        self._validate_children(design_object['children'], test_data)
        return self.errors

    def _validate_children(self, children: list, test_data: list):
        for child in children:
            self._validate_conditions(child, test_data)
            self._validate_children(child.get('children', []), test_data)

    def _validate_conditions(self, child: dict, test_data: list):
        if (validations := child.get('validation', [])) and child['visible']:
            for conditions_type, conditions in self._get_grouped_validation_conditions(validations).items():
                try:
                    validator = validation_condition_factory(conditions_type)
                    self.errors.extend(validator.validate(conditions, test_data, child['location']))
                except UnsupportedValidationConditionTypeError:
                    print(f'Conditions {conditions_type} skipped')

    @staticmethod
    def _get_grouped_validation_conditions(validation_conditions: list) -> dict:
        grouped_validation_conditions = collections.defaultdict(list)
        for condition in validation_conditions:
            grouped_validation_conditions[condition['type']].append(ValidationCondition(**condition))
        return grouped_validation_conditions
