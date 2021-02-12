from abc import ABCMeta, abstractmethod

from copy_cat.containers.errors_container import ErrorsContainer


class AbstractValidator(metaclass=ABCMeta):
    def __init__(self):
        self.errors_container = ErrorsContainer()

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass
