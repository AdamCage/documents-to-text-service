from uuid import UUID
from dataclasses import dataclass


@dataclass
class TextFromFilePipelineResult:
    id: UUID
    extracted_text: str
