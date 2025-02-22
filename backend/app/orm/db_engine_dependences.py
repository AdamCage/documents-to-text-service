import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.future import select
from dotenv import dotenv_values

from .models import Base, DocumentType
from utils import get_logger
from core import config, dict_tables_dict


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
        """Initialize the database schema and tables, and populate initial data."""
        async with self.engine.begin() as conn:
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {config.db_scheme};"))
            logger.info("DB schema created.")

            await conn.run_sync(Base.metadata.create_all)
            logger.info("DB tables created.")

        async with self.get_session() as session:
            # Начальные значения для DocumentType
            document_types = [
                {"document": "Паспорт РФ", "code": 1},
                {"document": "СНИЛС", "code": 2},
                {"document": "Заграничный паспорт РФ", "code": 3},
            ]

            for doc in document_types:
                existing_doc = await session.execute(select(DocumentType).filter_by(code=doc["code"]))
                if not existing_doc.scalars().first():
                    new_doc_type = DocumentType(document=doc["document"], code=doc["code"])
                    session.add(new_doc_type)
                    logger.info(f"Added document type: {doc['document']}")

            await session.commit()
            logger.info("DocumentType table populated.")


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
