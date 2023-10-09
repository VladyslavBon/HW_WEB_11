from datetime import date
from pydantic import BaseModel, EmailStr

class ContactBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: date

class ContactCreate(ContactBase):
    pass

class ContactResponce(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: date

    class Config:
        orm_mode = True