from copy_cat.models.base import BaseError


class Error(BaseError):
    fieldName: str
    designPath: str
    xpath: str
    errorMessage: str

    # parent: str   -> this can help on UI to show error

    def to_dict(self):
        return self.__dict__


Error.update_forward_refs()
