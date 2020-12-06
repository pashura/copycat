from copy_cat.models.test_data import DataObject
from copy_cat.models.validation_condition import Condition
from copy_cat.utils import get_test_data_object


def validate_condition(condition: Condition, test_data_obj: DataObject) -> bool:
    if condition.condition in ['present', 'required']:
        return True
    if condition.condition == 'equals':
        return test_data_obj.value == condition.value
    if condition.condition == 'minLength':
        return len(test_data_obj.value) >= int(condition.value)
    if condition.condition == 'maxLength':
        return len(test_data_obj.value) <= int(condition.value)


def get_successful_conditions_count(conditions: list[Condition], test_data: list[DataObject], location: str) -> int:
    count = 0
    for condition in conditions:
        test_data_obj = get_test_data_object(test_data, f'{location}/{condition.element}')
        count += bool(test_data_obj and validate_condition(condition, test_data_obj))
    return count
