from fastapi import Request
from fastapi.responses import JSONResponse

class UserNotFoundError(Exception):
    def __init__(self, email: str):
        self.email = email
        self.status_code = 404
        self.detail = f"User with email '{email}' not found"
        super().__init__(self.detail)


async def handle_user_not_found(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
