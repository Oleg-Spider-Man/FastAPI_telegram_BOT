import uvicorn

from fastapi import FastAPI
from api.routers import articul_rout
from api.routers.articul_rout import scheduler

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    scheduler.start()

app.include_router(articul_rout.router)


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

