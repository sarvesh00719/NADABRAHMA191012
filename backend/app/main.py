import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.db import init_db
from app.errors import AppError, app_error_handler
from app.routers import auth, me, checkins, activities, feedback, sessions, raga

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Nadbrahma API", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(AppError, app_error_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = request.headers.get("X-Request-ID", "unknown")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameters",
                "request_id": req_id
            }
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

app.include_router(auth.router, prefix="/api/v1")
app.include_router(me.router, prefix="/api/v1")
app.include_router(checkins.router, prefix="/api/v1")
app.include_router(activities.router, prefix="/api/v1")
app.include_router(feedback.router, prefix='/api/v1')
app.include_router(sessions.router, prefix='/api/v1')

@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "engine": settings.engine, "version": "1"}


