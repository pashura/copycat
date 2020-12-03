import re

from copy_cat.constants import XPATH_GROUPS_REGEX, XPATH_REP_REGEX
from copy_cat.utils import traverse_path_in_schema_object
from copy_cat.validators.choices_validator import ChoicesValidator
from copy_cat.validators.data_type_validator import DataTypeValidator
from copy_cat.validators.length_validator import LengthValidator
from copy_cat.validators.requirements_validator import RequirementsValidator


class Validator:
    def __init__(self):
        self.errors = []
        self.requirements_validator = RequirementsValidator()
        self.data_type_validator = DataTypeValidator()
        self.choices_validator = ChoicesValidator()
        self.length_validator = LengthValidator()

    def validate(self, test_data, schema):
        for ind, t in enumerate(test_data):
            location = t.get('location')[9:]
            location, reps = self._get_reps_and_location(location)

            el = traverse_path_in_schema_object(schema, location)
            if not el:
                print(location + " is not in design")
            else:
                self.data_type_validator.validate(el, t)
                self.length_validator.validate(el, t)
                self.choices_validator.validate(el, t)

        self.requirements_validator.validate(test_data, schema)
        self.errors += [
            *self.requirements_validator.errors, *self.data_type_validator.errors, *self.length_validator.errors,
            *self.choices_validator.errors
        ]

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
