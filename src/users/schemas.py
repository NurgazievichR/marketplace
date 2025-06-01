import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    # username: Optional[str]
    # first_name: Optional[str]
    # last_name: Optional[str]
    # middle_name: Optional[str]

class UserPublicSchema(UserBaseSchema):
    id: uuid.UUID
    # is_verified: bool
    # is_approved: bool

    class Config:
        orm_mode = True
