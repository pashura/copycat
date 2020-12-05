from copy_cat.models.error import Error
from copy_cat.singleton import Singleton


class ErrorsContainer(metaclass=Singleton):
    def __init__(self):
        self.__errors = []

    def errors(self) -> list:
        return [error.to_dict() for error in self.__errors]

    def append(self, error: Error):
        self.__errors.append(error)

    def extend(self, errors: list[Error]):
        self.__errors.extend(errors)
