from typing import Optional, List

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = ...
    price: int = Field(..., gt=0)
    model_name: str = ...
    rating: float = Field(..., ge=0.0, le=5.0)
    count: int = Field(..., ge=0)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Samsung A50',
                'price': 21000,
                'model_name': 'SM-A505F/DS',
                'rating': 4.5,
                'count': 100
            }
        }


class UpdateItem(BaseModel):
    name: Optional[str]
    price: Optional[int]
    model_name: Optional[str]
    rating: Optional[float]
    count: Optional[int]

    class Config:
        schema_extra = {
            'example': {
                'name': 'Samsung A50',
                'price': 21000,
                'model_name': 'SM-A505F/DS',
                'rating': 4.5,
                'count': 100
            }
        }


class Cart(BaseModel):
    # user: User
    items: Optional[List[Item]]
    total_price: int = 0


def ResponseModel(data, message):
    return {
        'data': [data],
        'code': 200,
        'message': message
    }


def ErrorResponseModel(error, code, message):
    return {
        'error': error,
        'code': code,
        'message': message
    }
