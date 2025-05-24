import uvicorn
from fastapi import FastAPI

from app.api import data_router
from app.db.base import Base
from app.db.session import engine

from app.services.check_service import do_check

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(data_router.router)


@app.post('/do_check')
async def do_address_check(address: str):
    return await do_check(address)


if __name__ == '__main__':
    uvicorn.run(app)
