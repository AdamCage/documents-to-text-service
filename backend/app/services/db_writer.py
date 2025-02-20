import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from orm import Request, Response, Extract
from utils import DBData, DataBaseWritingError


class DBWriter:
    """_summary_
    """

    def __init__(self, async_session: AsyncSession, upload_data: DBData, logger: logging.Logger) -> None:
        """_summary_

        Args:
            async_session (AsyncSession): _description_
            upload_data (DBData): _description_
        """
        self.async_session = async_session
        self.self.upload_data = upload_data
        self.logger = logger

        self.new_request__request_id = None
        self.new_response__id = None


    async def write_request(self) -> None:
        """Записать запрос в базу данных."""
        try:
            new_request = Request(request_id=self.upload_data.request_body.request_id, request_body=self.upload_data.request_body)

            self.async_session.add(new_request)
            await self.async_session.commit()
            await self.async_session.refresh(new_request)

            self.new_request__request_id = new_request.request_id

            self.logger.info(f"Request written successfully with ID: {self.new_request__request_id}")

        except Exception as e:
            await self.async_session.rollback()

            msg = f"Error writing request: {e}"
            self.logger.error(msg)
            raise DataBaseWritingError(msg)


    async def write_response(self) -> None:
        """Записать ответ в базу данных."""
        try:
            new_response = Response(
                request_id=self.new_request__request_id,
                response_code=self.upload_data.response_code,
                response_datetime=datetime.now()
            )

            self.async_session.add(new_response)
            await self.async_session.commit()
            await self.async_session.refresh(new_response)

            self.new_response__id = new_response.id

            self.logger.info(f"Response written successfully with ID: {self.new_response__id}")

        except Exception as e:
            await self.async_session.rollback()

            msg = f"Error writing response: {e}"
            self.logger.error(msg)
            raise DataBaseWritingError(msg)


    async def write_extract(self, image_number: int = 0) -> None:
        """Записать извлечение в базу данных.

        Args:
            image_number (int, optional): Номер изображения. Defaults to 0.
        """
        try:
            new_extract = Extract(
                image_number=image_number,
                original_image_s3_url=self.upload_data.original_image_s3_url,
                processed_image_s3_url=self.upload_data.processed_image_s3_url,
                extracted_text_s3_url=self.upload_data.extracted_text_s3_url,
                extracted_text=self.upload_data.extracted_text,
                response_id=self.new_response__id
            )

            self.async_session.add(new_extract)
            await self.async_session.commit()

            self.logger.info(f"Extract written successfully for image number: {image_number}")

        except Exception as e:
            await self.async_session.rollback()

            msg = f"Error writing extract: {e}"
            self.logger.error(msg)
            raise DataBaseWritingError(msg)


    async def write_all(self) -> None:
        """Записать все данные в базу данных."""
        await self.write_request()
        await self.write_response()
        await self.write_extract()
