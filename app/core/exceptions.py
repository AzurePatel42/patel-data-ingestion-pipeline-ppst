class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    pass


class ValidationException(AppException):
    pass


class UnsupportedDocumentException(ValidationException):
    pass


class EmptyDocumentException(ValidationException):
    pass


class EmbeddingProviderException(AppException):
    pass


class StorageException(AppException):
    pass