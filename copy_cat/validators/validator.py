import re

from copy_cat.constants import XPATH_GROUPS_REGEX, XPATH_REP_REGEX
from copy_cat.containers.errors_container import ErrorsContainer
from copy_cat.utils import traverse_path_in_schema_object
from copy_cat.validators.choices_validator import ChoicesValidator
from copy_cat.validators.data_type_validator import DataTypeValidator
from copy_cat.validators.length_validator import LengthValidator
from copy_cat.validators.requirements_validator import RequirementsValidator
from copy_cat.validators.validation_conditions.validator import ValidationConditionsValidator


class Validator:
    def __init__(self):
        self.errors_container = ErrorsContainer()
        self.requirements_validator = RequirementsValidator()
        self.data_type_validator = DataTypeValidator()
        self.choices_validator = ChoicesValidator()
        self.length_validator = LengthValidator()
        self.validation_conditions_validator = ValidationConditionsValidator()

    def validate(self, schema, test_data):
        for ind, t in enumerate(test_data):
            location = t.location[9:]
            location, reps = self._get_reps_and_location(location)

            el = traverse_path_in_schema_object(schema, location)
            if not el:
                print(location + " is not in design")
            else:
                self.errors_container.extend(self.data_type_validator.validate(el, t))
                self.errors_container.extend(self.length_validator.validate(el, t))
                self.errors_container.extend(self.choices_validator.validate(el, t))

        self.errors_container.extend(self.requirements_validator.validate(schema, test_data))
        self.errors_container.extend(self.validation_conditions_validator.validate(schema, test_data))

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
