from enum import Enum

from dataclasses import dataclass


@dataclass
class DocumentTypeElement:
    code: int
    name: str


class DocumentTypeEnum(Enum):
    OTHER = DocumentTypeElement(0, "Прочий документ")
    PASSPORT_RU = DocumentTypeElement(100, "Паспорт РФ")
    SNILS = DocumentTypeElement(101, "СНИЛС")
    FOREIGN_PASSPORT_RU = DocumentTypeElement(102, "Заграничный паспорт РФ")


    @classmethod
    def get_document_types(cls):
        return [{"document": doc.document.name, "code": doc.code} for doc in cls]


    @classmethod
    def from_code(cls, code):
        for doc in cls:
            if doc.code == code:
                return doc
            
        return None
