from typing import List

from copy_cat.core.validators.abstract_validator import AbstractValidator
from copy_cat.core.validators.choices_validator import ChoicesValidator
from copy_cat.core.validators.data_type_validator import DataTypeValidator
from copy_cat.core.validators.length_validator import LengthValidator
from copy_cat.core.validators.requirements_validator import RequirementsValidator
from copy_cat.models.design import DesignObject
from copy_cat.models.test_data import DataObject
from copy_cat.utils import get_reps_and_location


class Validator(AbstractValidator):
    def __init__(self):
        super().__init__()
        self.errors_container.clean()
        self.requirements_validator = RequirementsValidator()
        self.data_type_validator = DataTypeValidator()
        self.choices_validator = ChoicesValidator()
        self.length_validator = LengthValidator()

    def validate(self, design: DesignObject, test_data: List[DataObject]):
        for test_data_obj in test_data:
            location, reps = get_reps_and_location(test_data_obj.no_root_location)
            if not (design_object := design.get_child_by_location(location)):
                continue
            if design_object.visible:
                self.data_type_validator.validate(design_object, test_data_obj)
                self.length_validator.validate(design_object, test_data_obj)
                self.choices_validator.validate(design_object, test_data_obj)

        self.requirements_validator.validate(design, test_data)
