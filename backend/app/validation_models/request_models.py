from uuid import UUID
from typing import Literal, Optional

from pydantic import BaseModel


class ExtractTextFromImageRequestModel(BaseModel):
    id: UUID
    user_id: str = "user_1234"
    content_type: Literal["image/png", "image/jpeg", "image/jpg"] = "image/png"
    document_type_code: int = 100


class ExtractTextFromPDFRequestModel(BaseModel):
    id: UUID
    user_id: str = "user_1234"
    content_type: Literal["application/pdf"] = "application/pdf"
    document_type_code: int = 100


class ExtractTextFromImageWithLLMCorrectionRequestModel(ExtractTextFromImageRequestModel):
    custom_prompt: Optional[str] = None


class ExtractTextFromPDFWithLLMCorrectionRequestModel(ExtractTextFromPDFRequestModel):
    custom_prompt: Optional[str] = None
