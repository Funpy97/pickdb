""" Define common exceptions for pickdb pakage """


class DatabaseExistsError(Exception):
    def __init__(self, message: str):
        super(DatabaseExistsError, self).__init__(message)


class DatabaseNotFoundError(Exception):
    def __init__(self, message):
        super(DatabaseNotFoundError, self).__init__(message)


class TableExistsError(Exception):
    def __init__(self, message: str):
        super(TableExistsError, self).__init__(message)


class TableNotFoundError(Exception):
    def __init__(self, message: str):
        super(TableNotFoundError, self).__init__(message)


class RecordError(Exception):
    def __init__(self, message: str):
        super(RecordError, self).__init__(message)


class IdError(Exception):
    def __init__(self, message):
        super(IdError, self).__init__(message)


class ColumnExistsError(Exception):
    def __init__(self, message):
        super(ColumnExistsError, self).__init__(message)


class ColumnNotFoundError(Exception):
    def __init__(self, message):
        super(ColumnNotFoundError, self).__init__(message)