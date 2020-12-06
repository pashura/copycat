from copy_cat.utils import get_test_data_object
from copy_cat.validators.validation_conditions.errors_generator import ErrorsGenerator


class IfOneThenAllValidator:
    @staticmethod
    def validate(validations: list, test_data: list, location: str) -> list:
        errors = []
        for validation in validations:
            satisfied = True
            for condition in validation.rules[0].conditions:
                test_data_obj = get_test_data_object(test_data, f'{location}/{condition.element}')
                if not(test_data_obj and (not condition.value or condition.value == test_data_obj.value)):
                    satisfied = False
                    break

            if not satisfied:
                errors.append(ErrorsGenerator.generate(validation, location))

        return errors
