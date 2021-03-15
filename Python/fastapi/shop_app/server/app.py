from fastapi import FastAPI

from server.routes.item import router as item_router
from server.routes.cart import router as cart_router

app = FastAPI()

app.include_router(item_router, tags=['Item'], prefix='/item')
app.include_router(cart_router, tags=['Cart'], prefix='/cart')


@app.get('/', tags=['Root'])
async def root():
    return {'message': 'Welcome to the main page!'}
