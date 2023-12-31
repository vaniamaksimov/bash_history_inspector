class ApplicationError(Exception):
    ...


class GetHistoryError(ApplicationError):
    ...


class LogParseError(ApplicationError):
    ...


class NotSupportedOsError(ApplicationError):
    ...


class InvalidArgumentError(ApplicationError):
    ...


class NotSupportedModeError(ApplicationError):
    ...
