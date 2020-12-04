from copy_cat.validators.validation_conditions.at_least_one_of_validator import AtLeastOneOfValidator
from copy_cat.validators.validation_conditions.exceptions import UnsupportedValidationConditionTypeError


class ValidationConditions:
    AT_LEAST_ONE_OF = 'atLeastOneOf'


VALIDATION_CONDITION_CLASSES = {
    ValidationConditions.AT_LEAST_ONE_OF: AtLeastOneOfValidator,
}


def validation_condition_factory(validation_type: str):
    conditional_sourcing_type_class = VALIDATION_CONDITION_CLASSES.get(validation_type)
    if conditional_sourcing_type_class:
        return conditional_sourcing_type_class()
    raise UnsupportedValidationConditionTypeError()
