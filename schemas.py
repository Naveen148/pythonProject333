from pydantic import BaseModel
from .db import Base


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    lat: float
    lng: float

    class Config():
        orm_mode = True


class ShowAddress(BaseModel):
    lat: float
    lng: float

    class Config():
        orm_mode = True