from .enums import DocumentTypeEnum
from .llm_formater_promts import promts


class DocumentCodeLLMPromtMap:

    _mapping = {
        DocumentTypeEnum.PASSPORT_RU.value.code: promts.prompts["ru"]["passport_rf"],
        DocumentTypeEnum.SNILS.value.code: promts.prompts["ru"]["snils"],
        DocumentTypeEnum.FOREIGN_PASSPORT_RU.value.code: promts.prompts["ru"]["foreign_passport_rf"],
    }


    @classmethod
    def get_prompt(cls, code: int) -> str:
        """Получить промпт по коду документа."""
        return cls._mapping.get(code, None)
