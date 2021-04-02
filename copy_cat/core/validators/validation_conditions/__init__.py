from copy_cat.core.validators.validation_conditions.at_least_one_of_validator import (
    AtLeastOneOfValidator,
)
from copy_cat.core.validators.validation_conditions.exceptions import (
    UnsupportedValidationConditionTypeError,
)
from copy_cat.core.validators.validation_conditions.if_one_then_all_validator import (
    IfOneThenAllValidator,
)
from copy_cat.core.validators.validation_conditions.if_then_validator import (
    IfThenValidator,
)
from copy_cat.core.validators.validation_conditions.only_one_of_validator import (
    OnlyOneOfValidator,
)


class ValidationConditions:
    AT_LEAST_ONE_OF = "atLeastOneOf"
    IF_ONE_THEN_ALL = "ifOneThenAll"
    ONLY_ONE_OF = "onlyOneOf"
    IF_THEN = "ifThen"


VALIDATION_CONDITION_CLASSES = {
    ValidationConditions.AT_LEAST_ONE_OF: AtLeastOneOfValidator,
    ValidationConditions.IF_ONE_THEN_ALL: IfOneThenAllValidator,
    ValidationConditions.ONLY_ONE_OF: OnlyOneOfValidator,
    ValidationConditions.IF_THEN: IfThenValidator,
}


def validation_condition_factory(validation_type: str):
    conditional_sourcing_type_class = VALIDATION_CONDITION_CLASSES.get(validation_type)
    if conditional_sourcing_type_class:
        return conditional_sourcing_type_class()
    raise UnsupportedValidationConditionTypeError()
