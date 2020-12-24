import collections

from copy_cat.models.error import Error
from copy_cat.models.test_data import DataObject
from copy_cat.models.validation_condition import ValidationCondition
from copy_cat.utils import get_reps_and_location, get_test_data_object
from copy_cat.validators.abstract_validator import AbstractValidator
from copy_cat.validators.validation_conditions import (UnsupportedValidationConditionTypeError,
                                                       validation_condition_factory)


class RequirementsValidator(AbstractValidator):
    def __init__(self):
        super().__init__()
        self.result_parent = False
        self.result_children = False

    def validate(self, design_object: dict, test_data: list[DataObject]):
        active_paths = list(set([get_reps_and_location('/'.join(data_object.location.split('/')[1:-1]))[0]
                                 for data_object in test_data]))
        self._validate_conditions(design_object, test_data, active_paths)
        self._validate_children(design_object['children'], test_data, active_paths)

    def _validate_children(self, children: list, test_data: list[DataObject], active_paths):
        for child in children:
            if self._is_eligible_for_validation(child, active_paths):
                self._validate_requirements(child, test_data, active_paths)
                self._validate_conditions(child, test_data, active_paths)
            self._validate_children(child.get('children', []), test_data, active_paths)

    def _validate_conditions(self, design_object: dict, test_data: list[DataObject], active_paths):
        for c_type, conditions in self._get_grouped_validation_conditions(design_object.get('validation', [])).items():
            try:
                validator = validation_condition_factory(c_type)
                validator.validate(conditions, test_data, design_object['location'])
            except UnsupportedValidationConditionTypeError:
                print(f'Conditions {c_type} skipped')

    def _validate_requirements(self, design_object: dict, test_data: list[DataObject], active_paths):
        if not design_object.get('children') and not get_test_data_object(test_data, design_object.get('location')):
            # TODO: Fix error message to be similar to web xd
            error_message = f"Missing mandatory {design_object['name']} in {design_object['parent']['name']} record"
            self.errors_container.append(Error(fieldName="",
                                               designPath=design_object['location'],
                                               xpath="",
                                               errorMessage=error_message))

    @staticmethod
    def _get_grouped_validation_conditions(validation_conditions: list) -> dict:
        grouped_validation_conditions = collections.defaultdict(list)
        for condition in validation_conditions:
            grouped_validation_conditions[condition['type']].append(ValidationCondition(**condition))
        return grouped_validation_conditions

    def _is_eligible_for_validation(self, design_object, active_paths):
        if design_object.get('visible'):
            self.result_parent = False
            self.result_children = False
            self._check_parent(design_object, active_paths)
            self._check_children(design_object, active_paths)
            x = self.result_parent and (self.result_children or design_object.get('parent', {}).get(
                'minOccurs') > '0') and design_object.get('minOccurs') == '1'
            return x

    def _check_parent(self, design_object, active_paths):
        if parent := design_object.get('parent'):
            if parent.get('minOccurs'):
                self._check_parent(parent, active_paths)
            else:
                if '/'.join(parent.get('location').split('/')[:-1]) in active_paths:
                    self._check_parent(parent, active_paths)
        else:
            self.result_parent = True

    def _check_children(self, design_object, active_paths):
        if '/'.join(design_object.get('location', '').split('/')[:-1]) in active_paths:
            self.result_children = True
        elif children := design_object.get('children'):
            for child in children:
                self._check_children(child, active_paths)
