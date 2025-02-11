from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import get_async_session
from api.func import get_values, create_object, pars_wb
from api.operations import schemas, crud

from api.scheduler.scheduler_task import my_task

scheduler = AsyncIOScheduler()

router = APIRouter(
    prefix="/api_bot",
    tags=["api_bot"],
)


@router.post("/api/v1/products", response_model=schemas.ProductCreate)
async def collect_product_data(artikul_data: schemas.ProductArtikul, db: AsyncSession = Depends(get_async_session)):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/v1/subscribe/{artikul}",  response_model=schemas.ProductCreate)
async def get_product(artikul: str, db: AsyncSession = Depends(get_async_session)):
    try:
        scheduler.add_job(my_task, 'interval', minutes=1, args=[artikul, db], replace_existing=True)
        return await my_task(artikul, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))