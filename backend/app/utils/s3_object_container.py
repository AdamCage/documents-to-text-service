from dataclasses import dataclass

from dotenv import dotenv_values
import numpy as np

from validation_models import ExtractTextFromImageRequestModel, ExtractTextFromPDFRequestModel
from core import config, http_format


@dataclass
class S3Object:
    bytes: str
    s3_path: str
    url: str


@dataclass
class S3Objects:
    original: S3Object
    preprocessed: S3Object
    extracted_text: S3Object


    def __iter__(self):
        """Итератор для объектов S3, возвращающий имя атрибута и объект."""
        return iter(
            (
                ("original", self.original),
                ("preprocessed", self.preprocessed),
                ("extracted_text", self.extracted_text)
            )
        )



class S3ObjectsPathsAndUrls:
    """_summary_
    """

    def __init__(
            self,
            request_body: ExtractTextFromImageRequestModel | ExtractTextFromPDFRequestModel,
            image_number: int = 0
        ) -> None:
        """_summary_

        Args:
            request_body (ExtractTextFromImageRequestModel | ExtractTextFromPDFRequestModel,): _description_
            image_number (int, optional): _description_. Defaults to 0.
        """
        self.paths = self._create_paths(request_body, image_number)
        self.urls = self._create_urls()


    def _create_paths(
            self,
            request_body: ExtractTextFromImageRequestModel | ExtractTextFromPDFRequestModel,
            image_number: int
        ) -> dict[str, str]:
        """_summary_

        Args:
            request_body (ExtractTextFromImageRequestModel | ExtractTextFromPDFRequestModel): _description_
            image_number (int): _description_

        Returns:
            dict[str, str]: _description_
        """
        return {
            "original": f'{request_body.user_id}/{request_body.id}/original_file_{request_body.content_type.replace("/", ".")}',
            "processed_": f'{request_body.user_id}/{request_body.id}/processed_image_{image_number}_{request_body.content_type.replace("/", ".")}',
            "extracted_text": f'{request_body.user_id}/{request_body.id}/extracted_text.txt'
        }
    
    
    def _create_urls(self) -> dict[str, str]:
        """_summary_

        Returns:
            dict[str, str]: _description_
        """
        url = self._create_s3_url

        return {
            "original": f'{url}/{self.original_file_url}',
            "processed": f'{url}/{self.processed_image_url}',
            "extracted_text": f'{url}/{self.extracted_text_url}'
        }
    

    def _create_s3_url(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        host = dotenv_values["S3_HOST"]
        port = dotenv_values["S3_PORT"]
        bucket = config.s3_bucket_name

        return f'{http_format}://{host}:{port}/{bucket}'


def init_s3_objects(
        request: ExtractTextFromImageRequestModel | ExtractTextFromPDFRequestModel,
        image: np.ndarray,
        preprocessed_image: np.ndarray,
        extracted_text: str
    ) -> S3Objects:
    """_summary_

    Args:
        request (ExtractTextFromImageRequestModel | ExtractTextFromPDFRequestModel): _description_
        image (np.ndarray): _description_
        preprocessed_image (np.ndarray): _description_
        extracted_text (str): _description_

    Returns:
        S3Objects: _description_
    """
    s3_paths_and_urls = S3ObjectsPathsAndUrls(request)

    from services import bytes_converter

    return S3Objects(
        original=S3Object(
            bytes=bytes_converter.convert_file(image),
            s3_path=s3_paths_and_urls.paths["original"],
            url=s3_paths_and_urls.urls["original"]
        ),
        preprocessed=S3Object(
            bytes=bytes_converter.convert_file(preprocessed_image),
            s3_path=s3_paths_and_urls.paths["preprocessed"],
            url=s3_paths_and_urls.urls["preprocessed"]
        ),
        extracted_text=S3Object(
            bytes=bytes_converter.convert_string(extracted_text),
            s3_path=s3_paths_and_urls.paths["extracted_text"],
            url=s3_paths_and_urls.urls["extracted_text"]
        )
    )
