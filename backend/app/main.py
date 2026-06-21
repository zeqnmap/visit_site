from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.v1.routers import contact

# Инициализация базы данных при старте
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # В продакшене лучше использовать Alembic для миграций,
        # но для визитки create_all вполне подойдет.
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="ZEQnmap Portfolio API",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В продакшене замени на свой домен или localhost:5500
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Подключение роутеров
app.include_router(contact.router, prefix="/api/v1/contact", tags=["Contact"])