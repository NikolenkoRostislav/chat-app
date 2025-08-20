from fastapi import HTTPException
from functools import wraps

class AppError(Exception):
    pass

class InvalidEntryError(AppError):
    pass
    
class PermissionDeniedError(AppError):
    pass

class NotFoundError(AppError):
    pass

class AlreadyExistsError(AppError):
    pass 

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except InvalidEntryError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except PermissionDeniedError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except AlreadyExistsError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    return wrapper

__all__ = [
    "AppError",
    "InvalidEntryError",
    "PermissionDeniedError",
    "NotFoundError",
    "AlreadyExistsError"
]