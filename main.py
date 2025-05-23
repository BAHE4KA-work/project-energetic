import uvicorn
from fastapi import FastAPI

from app.api import data_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(data_router.router)


if __name__ == '__main__':
    uvicorn.run(app)
