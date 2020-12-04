from copy_cat.models.base import BaseError


class Error(BaseError):
    fieldName: str
    fieldPath: str
    xpath: str
    error: str

    # parent: str   -> this can help on UI to show error

    def to_dict(self):
        return self.__dict__


Error.update_forward_refs()
