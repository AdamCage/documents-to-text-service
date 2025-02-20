import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import dotenv_values

from .models import Base
from utils import get_logger
from core import config


logger = get_logger(__name__)


class DBEngine:
    """_summary_
    """
    
    def __init__(self, logger: logging.Logger) -> None:
        """_summary_

        Args:
            logger (logging.Logger): _description_
        """
        db_url = self.__get_database_url()

        self.engine = create_async_engine(
            db_url,
            echo=config.db_connection_pool["echo"],
            pool_size=config.db_connection_pool["pool_size"],
            max_overflow=config.db_connection_pool["max_overflow"],
            pool_timeout=config.db_connection_pool["pool_timeout"],
            pool_recycle=config.db_connection_pool["pool_recycle"]
        )
        logger.info("Database engine created.")

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)
        logger.info("Session pool created.")


    async def init_db(self):
        """_summary_
        """
        async with self.engine.begin() as conn:
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {config.db_scheme};"))
            logger.info("DB schema created.")

            await conn.run_sync(Base.metadata.create_all)
            logger.info("DB tables created.")


    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """_summary_

        Returns:
            AsyncGenerator[AsyncSession, None]: _description_

        Yields:
            Iterator[AsyncGenerator[AsyncSession, None]]: _description_
        """
        async with self.SessionLocal() as session:
            yield session


    def __get_database_url(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        DATABASE_CONFIG = dotenv_values()

        return f"postgresql+asyncpg://{DATABASE_CONFIG['DB_USER']}:{DATABASE_CONFIG['DB_PASSWORD']}@" \
            f"{DATABASE_CONFIG['DB_HOST']}:{DATABASE_CONFIG['DB_PORT']}/{DATABASE_CONFIG['DB_NAME']}"


db_engine = DBEngine(logger)
