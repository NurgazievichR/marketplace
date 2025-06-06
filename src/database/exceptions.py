import re

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

class UniqueConstraintViolation(Exception):
    def __init__(self, exc: IntegrityError, status_code: int = 409):
        self.status_code = status_code
        self.original_exception = exc
        self.fields = []
        self.input_values = {}
        self.detail = "Unique constraint violation"

        error_str = str(exc.orig)

        match = re.search(r'Key \((\w+)\)=\((.*?)\)', error_str)
        if match:
            field, value = match.groups()
            self.fields = [field]
            self.input_values = {field: value}

        super().__init__(self.detail)

async def handle_unique_violation(request: Request, exc: UniqueConstraintViolation):
    detail = []

    for field in exc.fields:
        detail.append({
            "type": "unique_error",
            "loc": ["body", field],
            "msg": f"The value for '{field}' already exists.",
            "input": exc.input_values.get(field)
        })

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": detail}
    )