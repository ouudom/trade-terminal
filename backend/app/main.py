from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.database import create_db_and_tables
from app.core.exceptions import (
    AppValidationError,
    ExternalServiceError,
    NotFoundError,
)
from app.core.logging import RequestLoggingMiddleware, configure_logging

from app.api.v1 import (
    instruments,
    forecast,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    create_db_and_tables()
    yield


app = FastAPI(title="Trade Terminal API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://trade-terminal.fireflowlabs.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)


# ── Exception handlers ────────────────────────────────────────────────────────

@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AppValidationError)
async def validation_handler(request, exc: AppValidationError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(ExternalServiceError)
async def ext_svc_handler(request, exc: ExternalServiceError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


# ── Routers ───────────────────────────────────────────────────────────────────

from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(instruments.router)
api_router.include_router(forecast.router)

app.include_router(api_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
