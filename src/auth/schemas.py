from pydantic import BaseModel, EmailStr, Field, model_validator

username_pattern = r'^[a-zA-Zа-яА-ЯёЁ0-9_]{3,32}$'

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=username_pattern)
    email: EmailStr = Field(max_length=256)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords don\'t match')
        return self
    
class LoginForm(BaseModel):
    username: str | None = Field(min_length=3, max_length=64, pattern=username_pattern)
    email: EmailStr | None = Field(max_length=256)
    password: str = Field(min_length=8, max_length=128)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"