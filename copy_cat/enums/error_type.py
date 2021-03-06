from enum import Enum


class ErrorType(Enum):
    CHOICES = 'choices'
    DATA_TYPE = 'dataType'
    FIELD_LENGTH = 'fieldLength'
    GROUP_LENGTH = 'groupLength'
    FIELD_REQUIREMENTS = 'fieldRequirements'
    GROUP_REQUIREMENTS = 'groupRequirements'

    COND_IF_THEN = 'conditionIfThen'
    COND_ONLY_ONE_OF = 'conditionOnlyOneOf'
    COND_AT_LEAST_ONE_OF = 'conditionAtLeastOneOf'
    COND_IF_ONE_THEN_ALL = 'conditionIfOneThenAll'

    def __str__(self):
        return str(self.value)
