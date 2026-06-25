from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
class UserResponse(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True

class UserMessageCreate(BaseModel):
    name: str
    email: str
    message: str

    