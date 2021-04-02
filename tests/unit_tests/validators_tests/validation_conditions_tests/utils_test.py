from unittest.mock import patch

from copy_cat.models.test_data import DataObject
from copy_cat.models.validation_condition import Condition, ValidationCondition
from copy_cat.core.validators.validation_conditions.utils import (
    get_successful_conditions_count,
    validate_condition,
)
from tests.unit_tests.validators_tests.validation_conditions_tests import (
    VALIDATION_CONDITION_IF_THEN_WITH_AND_CONJUNCTION,
)


@patch("copy_cat.core.validators.validation_conditions.utils.get_test_data_object")
@patch("copy_cat.core.validators.validation_conditions.utils.validate_condition")
def test_get_successful_conditions_count(
    mock_validate_condition, mock_get_test_data_object
):
    validation_condition = ValidationCondition(
        **VALIDATION_CONDITION_IF_THEN_WITH_AND_CONJUNCTION
    )
    test_data = []
    location = "location"
    mock_get_test_data_object.side_effect = [False, True, False, True]
    mock_validate_condition.side_effect = [True, False]
    actual = get_successful_conditions_count(
        validation_condition.results[0].conditions, test_data, location
    )
    expected = 1
    assert expected == actual


def test_validate_condition_present():
    condition = Condition(condition="present", element="element", value="")
    data_object = DataObject(text="")
    actual = validate_condition(condition, data_object)
    expected = True
    assert expected == actual


def test_validate_condition_required():
    condition = Condition(condition="required", element="element", value="")
    data_object = DataObject(text="")
    actual = validate_condition(condition, data_object)
    expected = True
    assert expected == actual


def test_validate_condition_equals_returns_true():
    condition = Condition(condition="equals", element="element", value="ZZ")
    data_object = DataObject(text="ZZ")
    actual = validate_condition(condition, data_object)
    expected = True
    assert expected == actual


def test_validate_condition_equals_returns_false():
    condition = Condition(condition="equals", element="element", value="")
    data_object = DataObject(text="ZZ")
    actual = validate_condition(condition, data_object)
    expected = False
    assert expected == actual


def test_validate_condition_min_length_returns_true():
    condition = Condition(condition="minLength", element="element", value="3")
    data_object = DataObject(text="ZZZ")
    actual = validate_condition(condition, data_object)
    expected = True
    assert expected == actual


def test_validate_condition_min_length_returns_false():
    condition = Condition(condition="minLength", element="element", value="3")
    data_object = DataObject(text="ZZ")
    actual = validate_condition(condition, data_object)
    expected = False
    assert expected == actual


def test_validate_condition_max_length_returns_false():
    condition = Condition(condition="maxLength", element="element", value="3")
    data_object = DataObject(text="ZZZZ")
    actual = validate_condition(condition, data_object)
    expected = False
    assert expected == actual


def test_validate_condition_max_length_returns_true():
    condition = Condition(condition="maxLength", element="element", value="3")
    data_object = DataObject(text="ZZZ")
    actual = validate_condition(condition, data_object)
    expected = True
    assert expected == actual
