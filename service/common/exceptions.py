from fastapi import HTTPException


class ObjectNotFound(HTTPException):
    def __init__(self, name: str):
        detail = f"{name} not found!"
        super().__init__(status_code=404, detail=detail)


class Unauthorized(HTTPException):
    def __init__(self, reason: str):
        detail = f"Unauthorized: {reason}."
        super().__init__(status_code=401, detail=detail)
