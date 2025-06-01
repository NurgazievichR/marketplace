# class AuthBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super().__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super().__call__(request)

#         if not credentials or credentials.scheme.lower() != "bearer":
#             raise HTTPException(status_code=403, detail="Invalid auth scheme.")

#         token = credentials.credentials

#         payload = get_payload(token)