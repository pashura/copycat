import re

from copy_cat.constants import XPATH_GROUPS_REGEX, XPATH_REP_REGEX
from copy_cat.utils import traverse_path_in_schema_object
from copy_cat.validators.abstract_validator import AbstractValidator
from copy_cat.validators.choices_validator import ChoicesValidator
from copy_cat.validators.data_type_validator import DataTypeValidator
from copy_cat.validators.length_validator import LengthValidator
from copy_cat.validators.requirements_validator import RequirementsValidator
from copy_cat.validators.validation_conditions.validator import ValidationConditionsValidator


class Validator(AbstractValidator):
    def __init__(self):
        super().__init__()
        self.errors_container.clean()
        self.requirements_validator = RequirementsValidator()
        self.data_type_validator = DataTypeValidator()
        self.choices_validator = ChoicesValidator()
        self.length_validator = LengthValidator()
        self.validation_conditions_validator = ValidationConditionsValidator()

    def validate(self, design, test_data):
        for test_data_obj in test_data:
            location = '/'.join(test_data_obj.location.split('/')[2:])
            location, reps = self._get_reps_and_location(location)

            design_object = traverse_path_in_schema_object(design, location)
            if not design_object:
                print(location + " is not in design")
            elif design_object.get('visible'):
                self.data_type_validator.validate(design_object, test_data_obj)
                self.length_validator.validate(design_object, test_data_obj)
                self.choices_validator.validate(design_object, test_data_obj)

        self.requirements_validator.validate(design, test_data)
        self.validation_conditions_validator.validate(design, test_data)

    @staticmethod
    def _get_reps_and_location(location):
        reps = []
        new_paths = []
        paths = location.split('/')
        for path in paths:
            if bool(re.search(XPATH_REP_REGEX, path)):
                groups = re.match(XPATH_GROUPS_REGEX, path).groups()
                reps.append({
                    "rep_name": groups[0],
                    "rep_number": groups[1]
                })
                new_paths.append(groups[0])
            else:
                new_paths.append(path)
        return '/'.join(new_paths), reps
