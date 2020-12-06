from copy_cat.models.validation_condition import ValidationCondition
from copy_cat.utils import get_test_data_object
from copy_cat.validators.validation_conditions.errors_generator import ErrorsGenerator


class IfThenValidator:
    def validate(self, validations: list, test_data: list, location: str) -> list:
        errors = []
        for validation in validations:
            if self._conditions_satisfied(validation, test_data, location):
                if not self._results_satisfied(validation, test_data, location):
                    errors.append(ErrorsGenerator.generate(validation, location))
        return errors

    @staticmethod
    def _results_satisfied(validation: ValidationCondition, test_data: list, location: str) -> bool:
        results = validation.results[0].conditions
        conjunction = validation.results[0].conjunction
        count = 0

        for result in results:
            test_data_obj = get_test_data_object(test_data, f'{location}/{result.element}')
            if test_data_obj:
                if result.condition == 'required':
                    count += 1
                elif result.condition == 'equals':
                    count += test_data_obj.value == result.value
                elif result.condition == 'minLength':
                    count += len(test_data_obj.value) >= int(result.value)
                elif result.condition == 'maxLength':
                    count += len(test_data_obj.value) <= int(result.value)

        return (conjunction == 'or' and count > 0) or (conjunction == 'and' and count == len(results))

    @staticmethod
    def _conditions_satisfied(validation: ValidationCondition, test_data: list, location: str) -> bool:
        conditions = validation.conditions[0].conditions
        conjunction = validation.conditions[0].conjunction
        count = 0

        for condition in conditions:
            test_data_obj = get_test_data_object(test_data, f'{location}/{condition.element}')
            if test_data_obj and (not condition.value or condition.value == test_data_obj.value):
                count += 1

        return (conjunction == 'or' and count > 0) or (conjunction == 'and' and count < len(conditions))
