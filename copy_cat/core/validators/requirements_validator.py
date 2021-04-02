import collections
from typing import List, Dict

from copy_cat.core.validators.abstract_validator import AbstractValidator
from copy_cat.core.validators.validation_conditions import (
    UnsupportedValidationConditionTypeError,
    validation_condition_factory,
)
from copy_cat.enums.error_type import ErrorType
from copy_cat.models.design import DesignObject
from copy_cat.models.error import Error
from copy_cat.models.test_data import DataObject
from copy_cat.models.validation_condition import ValidationCondition
from copy_cat.utils import get_reps_and_location, get_test_data_object


class RequirementsValidator(AbstractValidator):
    def __init__(self):
        super().__init__()
        self.result_parent = False
        self.result_children = False

    def validate(
        self, design_object: DesignObject, test_data: List[DataObject]
    ) -> None:
        active_paths = list(
            set(
                [
                    get_reps_and_location(
                        "/".join(data_object.location.split("/")[1:-1])
                    )[0]
                    for data_object in test_data
                ]
            )
        )
        self._validate_conditions(design_object, test_data)
        self._validate_children(design_object.children, test_data, active_paths)

    def _validate_children(
        self, children: List[DesignObject], test_data: List[DataObject], active_paths
    ) -> None:
        for child in children:
            if self._is_eligible_for_validation(child, active_paths):
                self._validate_record_requirements(child, test_data)
                self._validate_requirements(child, test_data)
                self._validate_conditions(child, test_data)
            self._validate_children(child.children, test_data, active_paths)

    def _validate_conditions(
        self, design_object: DesignObject, test_data: List[DataObject]
    ) -> None:
        for c_type, conditions in self._get_grouped_validation_conditions(
            design_object.validation
        ).items():
            try:
                validator = validation_condition_factory(c_type)
                if design_object.location:
                    validator.validate(conditions, test_data, design_object.location)
            except UnsupportedValidationConditionTypeError:
                print(f"Conditions {c_type} skipped")

    def _validate_record_requirements(
        self, design_object: DesignObject, test_data: List[DataObject]
    ) -> None:
        if design_object.children and not get_test_data_object(
            test_data, design_object.location
        ):
            error_message = f"Missing mandatory {design_object.name} record"
            self.errors_container.append(
                Error(
                    designPath=design_object.location,
                    errorMessage=error_message,
                    errorType=ErrorType.GROUP_REQUIREMENTS,
                )
            )
            design_object.skip_children = True

    def _validate_requirements(
        self, design_object: DesignObject, test_data: List[DataObject]
    ) -> None:
        if design_object.parent.skip_children:
            pass
        elif not design_object.children and not get_test_data_object(
            test_data, design_object.location
        ):
            # TODO: Fix error message to be similar to web xd
            error_message = f"Missing mandatory {design_object.name} in {design_object.parent.name} record"
            self.errors_container.append(
                Error(
                    designPath=design_object.location,
                    errorMessage=error_message,
                    errorType=ErrorType.FIELD_LENGTH,
                )
            )

    @staticmethod
    def _get_grouped_validation_conditions(validation_conditions: List) -> Dict:
        grouped_validation_conditions = collections.defaultdict(list)
        for condition in validation_conditions:
            grouped_validation_conditions[condition["type"]].append(
                ValidationCondition(**condition)
            )
        return grouped_validation_conditions

    def _is_eligible_for_validation(
        self, design_object: DesignObject, active_paths: List
    ) -> bool:
        if design_object.visible:
            self.result_parent = False
            self.result_children = False
            self._check_parent(design_object, active_paths)
            self._check_children(design_object, active_paths)
            return (
                self.result_parent
                and (self.result_children or design_object.parent.min_occurs > "0")
                and design_object.min_occurs == "1"
            )

    def _check_parent(self, design_object: DesignObject, active_paths: List) -> None:
        if parent := design_object.parent:
            if (
                parent.min_occurs
                or "/".join(parent.location.split("/")[:-1]) in active_paths
            ):
                self._check_parent(parent, active_paths)
        else:
            self.result_parent = True

    def _check_children(self, design_object: DesignObject, active_paths: List) -> None:
        if "/".join(design_object.location.split("/")[:-1]) in active_paths:
            self.result_children = True
        elif children := design_object.children:
            for child in children:
                self._check_children(child, active_paths)
