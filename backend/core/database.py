"""
Database configuration and initialization for MSP Alert Intelligence Platform
"""

import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel
import redis.asyncio as redis

from core.config import settings

logger = logging.getLogger(__name__)

# Database engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Redis connection
redis_client: redis.Redis = None


async def init_db():
    """Initialize database and create tables"""
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
        # Initialize Redis
        global redis_client
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        
        logger.info("Redis connection established")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis() -> redis.Redis:
    """Get Redis client"""
    if redis_client is None:
        raise RuntimeError("Redis client not initialized")
    return redis_client


async def close_db():
    """Close database connections"""
    await engine.dispose()
    if redis_client:
        await redis_client.close()
