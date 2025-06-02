from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

username_pattern = r'^[a-zA-Zа-яА-ЯёЁ0-9_]{3,32}$'

class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(max_length=256, examples=['user@admin.com'])
    password: str = Field(min_length=8, max_length=128, examples=['12345678'])
    confirm_password: str = Field(examples=['12345678'])

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords don\'t match')
        return self
    
class UserLoginSchema(BaseModel):
    email: EmailStr | None = Field(max_length=256, examples=['user@admin.com'])
    password: str = Field(min_length=8, max_length=128, examples=['12345678'])

class RefreshTokenSchema(BaseModel):
    refresh_token: str

class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOi...",
                "refresh_token": "dGhpc2lzYXJlZnJlc2h0b2tlbg==",
                "token_type": "bearer"
            }
        }
    )