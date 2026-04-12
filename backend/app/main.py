from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.routers.instruments import router as instruments_router
from app.routers.news import router as news_router
from app.routers.forexfactory import router as forexfactory_router
from app.routers.mt5 import router as mt5_router
from app.routers.bias import router as bias_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Trade Terminal API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(instruments_router)
app.include_router(news_router)
app.include_router(forexfactory_router)
app.include_router(mt5_router)
app.include_router(bias_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
