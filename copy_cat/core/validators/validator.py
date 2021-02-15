from copy_cat.utils import get_reps_and_location, traverse_path_in_schema_object
from copy_cat.core.validators.abstract_validator import AbstractValidator
from copy_cat.core.validators.choices_validator import ChoicesValidator
from copy_cat.core.validators.data_type_validator import DataTypeValidator
from copy_cat.core.validators.length_validator import LengthValidator
from copy_cat.core.validators.requirements_validator import RequirementsValidator


class Validator(AbstractValidator):
    def __init__(self):
        super().__init__()
        self.errors_container.clean()
        self.requirements_validator = RequirementsValidator()
        self.data_type_validator = DataTypeValidator()
        self.choices_validator = ChoicesValidator()
        self.length_validator = LengthValidator()

    def validate(self, design, test_data):
        for test_data_obj in test_data:
            location = '/'.join(test_data_obj.location.split('/')[2:])
            location, reps = get_reps_and_location(location)

            design_object = traverse_path_in_schema_object(design, location)
            if not design_object:
                print(location + " is not in design")
            elif design_object.get('visible'):
                self.data_type_validator.validate(design_object, test_data_obj)
                self.length_validator.validate(design_object, test_data_obj)
                self.choices_validator.validate(design_object, test_data_obj)

        self.requirements_validator.validate(design, test_data)
