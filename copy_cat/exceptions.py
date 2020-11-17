class ServiceError(Exception):
    """Base class for Exceptions in this module"""

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message', '')
        self.body = kwargs.pop('body', '')


class NotFoundError(ServiceError, FileNotFoundError):
    """Exception raised when resource is not found on the server"""


class DesignReaderException(ServiceError):
    """Exception raised when we have troubles inside DesignReader"""
