import httpx
from api.func import pars_wb, get_values, create_object
from api.operations import crud


async def my_task(artikul, db):
    async with (httpx.AsyncClient() as client):
        data = await pars_wb(artikul, client)
        keys_to_get = ['name', 'priceU', 'rating', 'totalQuantity']
        ready_data = get_values(data['data'], keys_to_get)
        product = create_object(artikul, ready_data)
        db_product = await crud.get_product_articul(db, product_articul=product.articul)
        if db_product:
            print("работает")
            return await crud.update_pr(db, product)
        db.add(product)
        await db.commit()
        return product
