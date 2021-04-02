from unittest.mock import patch

from copy_cat.enums.error_type import ErrorType
from copy_cat.models.error import Error
from copy_cat.models.validation_condition import ValidationCondition
from copy_cat.core.validators.validation_conditions import OnlyOneOfValidator
from tests.unit_tests.validators_tests.validation_conditions_tests import (
    VALIDATION_CONDITION_WITH_RULES,
)


class TestOnlyOneOfValidator:
    def setup_method(self):
        self.validator = OnlyOneOfValidator()
        self.test_data = []
        self.location = "location"
        self.validation_condition = ValidationCondition(
            **VALIDATION_CONDITION_WITH_RULES
        )

    @patch.object(OnlyOneOfValidator, "_conditions_satisfied")
    @patch(
        "copy_cat.core.validators.validation_conditions.only_one_of_validator.ErrorsGenerator.generate"
    )
    def test_validate(self, mock_generate, mock__rules_satisfied):
        expected = len(self.validator.errors_container.errors()) + 1
        mock_validations = [self.validation_condition, self.validation_condition]
        mock__rules_satisfied.side_effect = [True, False]
        mock_generate.return_value = Error(
            fieldName="",
            designPath=self.location,
            xpath="",
            errorMessage="1",
            errorType=ErrorType.COND_ONLY_ONE_OF,
        )
        self.validator.validate(mock_validations, self.test_data, self.location)
        assert expected == len(self.validator.errors_container.errors())

    @patch(
        "copy_cat.core.validators.validation_conditions.only_one_of_validator.get_successful_conditions_count"
    )
    def test__conditions_satisfied_returns_true(
        self, mock_get_successful_conditions_count
    ):
        mock_get_successful_conditions_count.return_value = 1
        actual = self.validator._conditions_satisfied(
            self.validation_condition.rules[0], self.test_data, self.location
        )
        expected = True
        assert expected == actual

    @patch(
        "copy_cat.core.validators.validation_conditions.only_one_of_validator.get_successful_conditions_count"
    )
    def test__conditions_satisfied_returns_false(
        self, mock_get_successful_conditions_count
    ):
        mock_get_successful_conditions_count.return_value = 2
        actual = self.validator._conditions_satisfied(
            self.validation_condition.rules[0], self.test_data, self.location
        )
        expected = False
        assert expected == actual
