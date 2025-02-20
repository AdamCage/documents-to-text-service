from pydantic import BaseModel

class ExtractTextFromImageResponseModel(BaseModel):
    request_id: str
    response_id: str
    extracted_text: str


class ExtractTextFromPDFResponseModel(BaseModel):
    request_id: str
    response_id: str
    extracted_text: str
