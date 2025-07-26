class AppError(Exception):
    pass

class PermissionDeniedError(AppError):
    pass

class NotFoundError(AppError):
    pass

class AlreadyExistsError(AppError):
    pass 

class InvalidEntryError(AppError):
    pass