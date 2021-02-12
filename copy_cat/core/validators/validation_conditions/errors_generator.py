from copy_cat.models.error import Error
from copy_cat.models.validation_condition import ValidationCondition

CONDITIONS_CONVERSIONS = {
    'present': ' is present',
    'equals': ' is equal to ',
}

RESULTS_CONVERSIONS = {
    'required': ' is required',
    'equals': ' must be equal to ',
    'minLength': ' minimum length is ',
    'maxLength': ' maximum length is '
}


class ErrorsGenerator:
    @staticmethod
    def generate(validation: ValidationCondition, location: str) -> Error:
        return {
            'ifThen': ErrorsGenerator._generate_if_then_error,
            'ifOneThenAll': ErrorsGenerator._generate_if_one_then_all_error,
            'atLeastOneOf': ErrorsGenerator._generate_at_least_one_of_error,
            'onlyOneOf': ErrorsGenerator._generate_only_one_of_error,
        }.get(validation.type)(validation, location)

    @staticmethod
    def _generate_if_then_error(validation: ValidationCondition, location: str) -> Error:
        conditions_conjunction = f" {validation.conditions[0].conjunction} "
        results_conjunction = f" {validation.results[0].conjunction} "
        conditions_elements = ErrorsGenerator.__get_elements_from_conditions(validation)
        results_elements = ErrorsGenerator.__get_elements_from_results(validation)
        error_message = f'If {conditions_conjunction.join(conditions_elements)}, ' \
                        f'then {results_conjunction.join(results_elements)}'
        return Error(fieldName="", designPath=location, xpath="", errorMessage=error_message)

    @staticmethod
    def _generate_if_one_then_all_error(validation: ValidationCondition, location: str) -> Error:
        conjunction = f" {validation.rules[0].conjunction} "
        elements = ErrorsGenerator.__get_elements_from_rules(validation)
        error_message = f'If {conjunction.join(elements)} is present, then all are required'
        return Error(fieldName="", designPath=location, xpath="", errorMessage=error_message)

    @staticmethod
    def _generate_at_least_one_of_error(validation: ValidationCondition, location: str) -> Error:
        conjunction = f" {validation.rules[0].conjunction} "
        elements = ErrorsGenerator.__get_elements_from_rules(validation)
        error_message = f'At least one of {conjunction.join(elements)} is required'
        return Error(fieldName="", designPath=location, xpath="", errorMessage=error_message)

    @staticmethod
    def _generate_only_one_of_error(validation: ValidationCondition, location: str) -> Error:
        conjunction = f" {validation.rules[0].conjunction} "
        elements = ErrorsGenerator.__get_elements_from_rules(validation)
        error_message = f'Only one of {conjunction.join(elements)} can be present'
        return Error(fieldName="", designPath=location, xpath="", errorMessage=error_message)

    @staticmethod
    def __get_elements_from_rules(validation: ValidationCondition) -> list:
        return [
            f'{el.element}{CONDITIONS_CONVERSIONS[el.condition] + el.value if el.value else ""}' for el in
            validation.rules[0].conditions
        ]

    @staticmethod
    def __get_elements_from_results(validation: ValidationCondition) -> list:
        return [
            f'{el.element}{RESULTS_CONVERSIONS[el.condition]}{el.value if el.value else ""}' for el in
            validation.results[0].conditions
        ]

    @staticmethod
    def __get_elements_from_conditions(validation: ValidationCondition) -> list:
        return [
            f'{el.element}{CONDITIONS_CONVERSIONS[el.condition]}{el.value if el.value else ""}' for el in
            validation.conditions[0].conditions
        ]
