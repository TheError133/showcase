from fastapi import APIRouter

from server.database import (
    add_item_to_cart,
    remove_item_from_cart
)
from server.models import (
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()


@router.post('/{id}', response_description='Item added to cart')
async def add_item_data_to_cart(id: str):
    success, message = await add_item_to_cart(id)
    if success:
        return ResponseModel(message, 'Item added to cart successfully')
    return ErrorResponseModel(
        'An error occurred while adding item to cart.',
        404,
        message
    )


@router.put('/{id}', response_description='Item removed from cart')
async def remove_item_data_from_cart(id: str):
    success, message = await remove_item_from_cart(id)
    if success:
        return ResponseModel(message, 'Item removed from cart successfully')
    return ErrorResponseModel(
        'An error occurred while removing item from cart.',
        404,
        message
    )
