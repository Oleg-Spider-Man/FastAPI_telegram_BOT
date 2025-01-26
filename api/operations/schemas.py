from pydantic import BaseModel


class ProductArtikul(BaseModel):
    artikul: str


class ProductCreate(BaseModel):
    articul: str
    name: str
    price: float
    rating: float
    total_quantity: int

    class Config:
        orm_mode = True
