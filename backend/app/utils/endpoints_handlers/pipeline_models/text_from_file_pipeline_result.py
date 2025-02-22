from dataclasses import dataclass


@dataclass
class TextFromFilePipelineResult:
    extracted_text: str
    response_id: str
