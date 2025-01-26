import httpx
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import get_async_session
from api.func import get_values, create_object, pars_wb
from api.operations import schemas, crud
from api.scheduler.scheduler_con import scheduler
from api.scheduler.scheduler_task import my_task


app = FastAPI()


@app.post("/api/v1/products", response_model=schemas.ProductCreate)
async def collect_product_data(artikul_data: schemas.ProductArtikul, db: AsyncSession = Depends(get_async_session)):
    async with (httpx.AsyncClient() as client):
        artikul = artikul_data.artikul
        data = await pars_wb(artikul, client)
        keys_to_get = ['name', 'priceU', 'rating', 'totalQuantity']
        ready_data = get_values(data['data'], keys_to_get)
        product = create_object(artikul, ready_data)
        db_product = await crud.get_product_articul(db, product_articul=product.articul)
        if db_product:
            return await crud.update_pr(db, product)
        db.add(product)
        await db.commit()
        return product


@app.get("/api/v1/subscribe/{artikul}",  response_model=schemas.ProductCreate)
async def get_product(artikul: str, db: AsyncSession = Depends(get_async_session)):
    scheduler.add_job(my_task, 'interval', minutes=1, args=[artikul, db], replace_existing=True)
    return await my_task(artikul, db)


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

