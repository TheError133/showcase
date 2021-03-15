import os

import motor.motor_asyncio
from bson.objectid import ObjectId

env = os.getenv

db_user = env('db_user')
db_pass = env('db_pass')
db_ip = env('db_ip')
db_port = env('db_port')

MONGO_DETAILS = 'mongodb://{}:{}@{}:{}'.format(db_user, db_pass, db_ip, db_port)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.main

item_collection = database.get_collection('shop')
cart_collection = database.get_collection('cart')


# Helpers.
def item_helper(item) -> dict:
    return {
        'id': str(item.get('_id')),
        'name': item.get('name'),
        'price': item.get('price'),
        'model_name': item.get('model_name'),
        'rating': item.get('rating'),
        'count': item.get('count')
    }


def cart_helper(cart) -> dict:
    return {
        'id': str(cart.get('_id')),
        # 'user': cart.get('user'),
        'items': cart.get('items'),
        'total_price': cart.get('total_price')
    }


# CRUD.
# Товары.
async def retrieve_items():
    """Получение списка товаров."""
    items = []
    async for item in item_collection.find():
        items.append(item_helper(item))

    return items


async def retrieve_item(id: str) -> dict:
    """Получение информации по одному товару."""
    item = await item_collection.find_one({'_id': ObjectId(id)})
    if item:
        return item_helper(item)


async def add_item(item_info: dict) -> dict:
    """Добавление информации по товару."""
    item = await item_collection.insert_one(item_info)
    result_item = await item_collection.find_one({'_id': item.inserted_id})

    return item_helper(result_item)


async def update_item(id: str, data: dict):
    """Обновление информации по товару."""
    # Если данные не переданы, возвращаем False.
    if len(data) < 1:
        return False

    item = await item_collection.find_one({'_id': ObjectId(id)})
    if item:
        updated_item = await item_collection.update_one(
            {'_id': ObjectId(id)}, {'$set': data} 
        )
        
        if updated_item:
            return True
        return False


async def delete_item(id: str):
    """Удаление товара из базы."""
    item = await item_collection.find_one({'_id': ObjectId(id)})
    if item:
        await item_collection.delete_one({'_id': ObjectId(id)})
        return True


# Корзина.
async def add_item_to_cart(id: str):
    """Добавление товара в корзину."""
    # Получение товара по id.
    item = await item_collection.find_one({'_id': ObjectId(id)})
    # Если товара не существует, то выходим.
    if not item:
        return False, f'Item with ID: {id} doesn\'t exist'
    # Проверка наличия корзины.
    cart = await cart_collection.find_one()
    if not cart:
        await cart_collection.insert_one({'items': [], 'total_price': 0})
        cart = await cart_collection.find_one()
    # Обновление информации.
    new_cart_items = cart.get('items')
    new_cart_items.append(item)
    new_total_price = cart.get('total_price') + item.get('price')
    updated_cart = await cart_collection.update_one(
        {'_id': cart.get('_id')}, {'$set': {'items': new_cart_items, 'total_price': new_total_price}}
    )

    if updated_cart:
        return True, f'Item with ID: {id} added to cart'
    return False, 'Error adding item to cart'


async def remove_item_from_cart(id: str):
    """Удаление товара из корзины."""
    # Получение товара по id.
    item = await item_collection.find_one({'_id': ObjectId(id)})
    # Если товара не существует, то выходим.
    if not item:
        return False, f'Item with ID: {id} doesn\'t exist'
    cart = await cart_collection.find_one()
    # Если корзины нет, то сразу выходим.
    if not cart:
        return False, 'Cart is empty'
    # Обновление информации.
    cart_items = cart.get('items')
    cart_total_price = cart.get('total_price')
    if item in cart_items:
        cart_items.remove(item)
        cart_total_price -= item.get('price')
        await cart_collection.update_one(
            {'_id': cart.get('_id')}, {'$set': {'items': cart_items, 'total_price': cart_total_price}}
        )
        return True, f'Item with ID: {id} removed from cart'
    return False, f'Item with ID: {id} doesn\'t exist in cart'        
