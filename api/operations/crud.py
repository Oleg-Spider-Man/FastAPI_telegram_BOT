from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.operations import models, schemas
from api.operations.models import Product


async def get_product_articul(db: AsyncSession, product_articul: str):
    query = select(models.Product).filter(models.Product.articul == product_articul)
    result = await db.execute(query)
    return result.scalar()


async def update_pr(db: AsyncSession, product: schemas.ProductCreate):
    update_p = update(Product).where(Product.articul == product.articul).values(
        articul=product.articul,
        name=product.name,
        price=product.price,
        rating=product.rating,
        total_quantity=product.total_quantity
    )
    await db.execute(update_p)
    await db.commit()
    return product
