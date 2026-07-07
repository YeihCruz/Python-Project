class ServiceError(Exception):
    """Base exception for service layer errors."""


class NotFoundError(ServiceError):
    """Raised when a requested record does not exist."""


class ValidationError(ServiceError):
    """Raised when input data fails validation rules."""


class DuplicateError(ServiceError):
    """Raised when a unique constraint would be violated."""


class BusinessRuleError(ServiceError):
    """Raised when a domain/business rule is violated."""


class RelatedRecordsExistError(ServiceError):
    """Raised when trying to delete a record that has related data."""
