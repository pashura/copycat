from copy_cat.enums.error_type import ErrorType
from copy_cat.models.base import BaseError


# TODO: snake case here + add alias
class Error(BaseError):
    fieldName: str
    designPath: str
    xpath: str
    errorMessage: str

    errorType: ErrorType

    # parent: str   -> this can help on UI to show error

    def to_dict(self):
        return self.__dict__


Error.update_forward_refs()
