from pydantic import BaseModel


class LLMRequest(BaseModel):
    stream: bool
    model: str
    format: str
    prompt: str
