from pydantic import BaseModel, EmailStr, Field, model_validator

username_pattern = r'^[a-zA-Zа-яА-ЯёЁ0-9_]{3,32}$'

class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=256, examples=['user@admin.com'])
    password: str = Field(min_length=8, max_length=128, examples=['12345678'])
    confirm_password: str = Field(min_length=8, max_length=128, examples=['12345678'])

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords don\'t match')
        return self
    
class LoginForm(BaseModel):
    email: EmailStr | None = Field(max_length=256, examples=['user@admin.com'])
    password: str = Field(min_length=8, max_length=128, examples=['12345678'])

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "dGhpc2lzYXJlZnJlc2h0b2tlbg==",
                "token_type": "bearer"
            }
        }