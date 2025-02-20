import logging
from contextlib import contextmanager
from io import BytesIO

import boto3
from botocore.client import BaseClient 
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import dotenv_values

from utils import get_logger, S3UploadingError, S3Objects
from core import config


logger = get_logger(__name__)


class S3Uploader:
    """Сервис для загрузки файлов в Amazon S3."""

    def __init__(self, bucket_name: str, logger: logging.Logger) -> None:
        self.bucket_name = bucket_name
        self.logger = logger


    def upload_objects(self, objects: S3Objects):
        with self._create_s3_client() as s3_client:
            for object_name, obj in objects:
                obj_bytes = obj.bytes
                s3_path = obj.s3_path

                try:
                    self._upload_fileobj(obj_bytes, object_name, s3_path, s3_client)

                except NoCredentialsError:
                    msg = "Credentials not available"
                    self.logger.error(msg)
                    raise S3UploadingError(msg)
                
                except ClientError as e:
                    msg = f"Client failed to upload file: {e}"
                    self.logger.error(msg)
                    raise S3UploadingError(msg)
                
                except Exception as e:
                    msg = f"Failed to upload file: {e}"
                    self.logger.error(msg)
                    raise S3UploadingError(msg)  

            logger.info("Objects successfully loaded into S3")


    @contextmanager
    def _create_s3_client(self):
        """Создать клиента S3 с использованием учетных данных из .env."""
        config = dotenv_values()
        
        s3_access_key_id = config.get("s3_access_key_id")
        s3_secret_access_key = config.get("s3_secret_access_key")

        session = boto3.Session(
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key
        )

        s3_client = session.client('s3')
    
        try:
            yield s3_client

        finally:
            pass


    def _upload_fileobj(self, file_obj: BytesIO, object_name: str, s3_path: str, s3_client: BaseClient) -> str:
        """_summary_

        Args:
            file_obj (BytesIO): _description_
            object_name (str): _description_
            s3_client (BaseClient): _description_

        Returns:
            str: _description_
        """
        file_obj.seek(0)
        s3_client.upload_fileobj(file_obj, self.bucket_name, s3_path)
        self.logger.info(f"File {object_name} uploaded successfully to {s3_path}.")


s3_uploader = S3Uploader(bucket_name=config.s3_bucket_name, logger=logger)
