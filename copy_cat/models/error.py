from copy_cat.models.base import BaseError


class Error(BaseError):
    error: str
    fieldName: str
    fieldPath: str
    xpath: str
    # parent: str   -> this can help on UI to show error


Error.update_forward_refs()
