from pydantic import BaseModel, EmailStr, Field, model_validator

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr = Field(max_length=256)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords don\'t match')
        return self