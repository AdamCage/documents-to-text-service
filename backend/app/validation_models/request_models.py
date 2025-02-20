from typing import Literal

from pydantic import BaseModel


class ExtractTextFromImageRequestModel(BaseModel):
    id: str
    user_id: str
    content_type: Literal["image/png", "image/jpeg", "image/jpg"]


class ExtractTextFromPDFRequestModel(BaseModel):
    id: str
    user_id: str
    content_type: Literal["application/pdf"]
