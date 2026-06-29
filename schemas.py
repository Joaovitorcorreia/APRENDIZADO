from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserMessageCreate_and_response(BaseModel):
    name: str | None
    email: EmailStr
    message: str

class UserAtualizar(BaseModel):
    new_name: str = Field(..., min_length=1, max_length=100)
    new_email: EmailStr

class UserAtualizarResponse(BaseModel):
    new_name: str
    new_email: EmailStr
    message: str

class UserDelete(BaseModel):
    email: EmailStr

class UserDeleteResponse(BaseModel):
    email: EmailStr
    message: str
    class Config:
        from_attributes = True