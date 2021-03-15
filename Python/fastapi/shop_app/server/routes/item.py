from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_items,
    retrieve_item,
    add_item,
    update_item,
    delete_item
)
from server.models import (
    ErrorResponseModel,
    ResponseModel,
    Item,
    UpdateItem
)

router = APIRouter()


@router.post('/', response_description='Item data added to database')
async def add_item_data(item: Item = Body(...)):
    item = jsonable_encoder(item)
    new_item = await add_item(item)
    return ResponseModel(new_item, 'Item added successfully')


@router.get('/', response_description='Items retrieved')
async def get_items():
    items = await retrieve_items()
    if items:
        return ResponseModel(items, 'Items data retrieved successfully')
    return ResponseModel(items, 'Empty list returned')


@router.get('/{id}', response_description='Item data retrieved')
async def get_item(id: str):
    item = await retrieve_item(id) 
    if item:
        return ResponseModel(item, 'Item data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, 'Idem doesn\'t exist')


@router.put('/{id}')
async def update_item_data(id: str, req: UpdateItem = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_item = await update_item(id, req)
    if updated_item:
        return ResponseModel(
            f'Item with ID: {id} name update is successful',
            'Item name updated successfully'
        )
    return ErrorResponseModel(
        'An error occurred',
        404,
        'There was an error updating item data'
    )


@router.delete('/{id}', response_description='Item data deleted from database')
async def delete_item_data(id: str):
    deleted_item = await delete_item(id)
    if deleted_item:
        return ResponseModel(f'Item with ID: {id} was deleted', 'Item deleted successfully')
    return ErrorResponseModel('An error occurred.', 404, f'Item with ID: {id} doesn\'t exist')
