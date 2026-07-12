class AppException(Exception):
    """Base exception for all application errors."""
    pass


class NotFoundException(AppException):
    """Raised when a requested resource cannot be found."""

    def __init__(self, message: str):
        self.message = message