from unittest.mock import patch

from copy_cat.models.error import Error
from copy_cat.models.validation_condition import ValidationCondition
from copy_cat.validators.validation_conditions import IfThenValidator
from tests.unit_tests.validators_tests.validation_conditions_tests import (
    VALIDATION_CONDITION_IF_THEN_WITH_AND_CONJUNCTION,
    VALIDATION_CONDITION_IF_THEN_WITH_OR_CONJUNCTION
)


class TestIfThenValidator:

    def setup_method(self):
        self.validator = IfThenValidator()
        self.test_data = []
        self.location = 'location'
        self.validation_condition_or = ValidationCondition(**VALIDATION_CONDITION_IF_THEN_WITH_OR_CONJUNCTION)
        self.validation_condition_and = ValidationCondition(**VALIDATION_CONDITION_IF_THEN_WITH_AND_CONJUNCTION)

    @patch.object(IfThenValidator, '_conditions_satisfied')
    @patch('copy_cat.validators.validation_conditions.if_then_validator.ErrorsGenerator.generate')
    def test_validate(self, mock_generate, mock__conditions_satisfied):
        expected = len(self.validator.errors_container.errors()) + 1
        mock_validations = [self.validation_condition_or, self.validation_condition_and]
        mock__conditions_satisfied.side_effect = [True, False, False, True]
        mock_generate.return_value = Error(fieldName="", designPath=self.location, xpath="", errorMessage='1')
        self.validator.validate(mock_validations, self.test_data, self.location)
        assert expected == len(self.validator.errors_container.errors())

    @patch('copy_cat.validators.validation_conditions.if_then_validator.get_successful_conditions_count')
    def test__conditions_satisfied__or_returns_true_when_count_is_not_zero(self, mock_get_successful_conditions_count):
        mock_get_successful_conditions_count.return_value = 1
        conditions = self.validation_condition_or.conditions[0]
        actual = self.validator._conditions_satisfied(conditions, self.test_data, self.location)
        expected = True
        assert expected == actual

    @patch('copy_cat.validators.validation_conditions.if_then_validator.get_successful_conditions_count')
    def test__conditions_satisfied__or_returns_false_when_count_is_zero(self, mock_get_successful_conditions_count):
        mock_get_successful_conditions_count.return_value = 0
        conditions = self.validation_condition_or.conditions[0]
        actual = self.validator._conditions_satisfied(conditions, self.test_data, self.location)
        expected = False
        assert expected == actual

    @patch('copy_cat.validators.validation_conditions.if_then_validator.get_successful_conditions_count')
    def test__conditions_satisfied__and_returns_true_when_count_equals_conditions_len(
            self, mock_get_successful_conditions_count
    ):
        mock_get_successful_conditions_count.return_value = 2
        conditions = self.validation_condition_or.conditions[0]
        actual = self.validator._conditions_satisfied(conditions, self.test_data, self.location)
        expected = True
        assert expected == actual

    @patch('copy_cat.validators.validation_conditions.if_then_validator.get_successful_conditions_count')
    def test__conditions_satisfied__and_returns_false_when_count_does_not_equals_conditions_len(
            self, mock_get_successful_conditions_count
    ):
        mock_get_successful_conditions_count.return_value = 0
        conditions = self.validation_condition_or.conditions[0]
        actual = self.validator._conditions_satisfied(conditions, self.test_data, self.location)
        expected = False
        assert expected == actual
