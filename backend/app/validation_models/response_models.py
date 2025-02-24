from uuid import UUID

from pydantic import BaseModel


class ExtractTextFromImageResponseModel(BaseModel):
    request_id: UUID
    response_id: UUID
    extracted_text: str = (
        "Российская Федерация СТРАХОВОЕ СВИДЕТЕХЬСТВО ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО "
        "СТРАХОВАНИЯ 038-451-033 48 Ф.и.0 ИВАНОВА СВЕТДАНА ИВАНОВНА Дата и место "
        "рождения 21 августа 1963 года АНГАРСК ИРКУТСКАЯ ОБЛАСТЬ Пол ЖенсКий "
        "Дата регистрации 29 сентября 1998 года"
    )

class ExtractTextFromPDFResponseModel(BaseModel):
    request_id: UUID
    response_id: UUID
    extracted_text: str = (
        "Российская Федерация СТРАХОВОЕ СВИДЕТЕХЬСТВО ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО "
        "СТРАХОВАНИЯ 038-451-033 48 Ф.и.0 ИВАНОВА СВЕТДАНА ИВАНОВНА Дата и место "
        "рождения 21 августа 1963 года АНГАРСК ИРКУТСКАЯ ОБЛАСТЬ Пол ЖенсКий "
        "Дата регистрации 29 сентября 1998 года"
    )


class ExtractTextFromImageWithLLMCorrectionResponseModel(BaseModel):
    request_id: UUID
    response_id: UUID
    extracted_text: str = (
        "Российская Федерация СТРАХОВОЕ СВИДЕТЕХЬСТВО ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО "
        "СТРАХОВАНИЯ 038-451-033 48 Ф.и.0 ИВАНОВА СВЕТДАНА ИВАНОВНА Дата и место "
        "рождения 21 августа 1963 года АНГАРСК ИРКУТСКАЯ ОБЛАСТЬ Пол ЖенсКий "
        "Дата регистрации 29 сентября 1998 года"
    )
    llm_corrected_text: str = (
        '{"snils_number": "038-451-033 48", '
        '"last_name": "Иванова", '
        '"name": "Светлана", '
        '"surname": "Ивановна", '
        '"birth_date": "21 августа 1963 года", '
        '"birth_place": "АНГАРСК ИРКУТСКАЯ ОБЛАСТЬ", '
        '"gender": "женский", '
        '"registration_date": "29 сентября 1998 года", '
        '"is_corrected": true, '
        '"corrections": ['
        '  {"original_word": "СВЕТДАНА", "corrected_word": "Светлана"}, '
        '  {"original_word": "ЖенсКий", "corrected_word": "женский"}, '
        '  {"original_word": "ИКУТСКАЯ", "corrected_word": "ИРКУТСКАЯ"}'
        '] }'
    )


class ExtractTextFromPDFWithLLMCorrectionResponseModel(BaseModel):
    request_id: UUID
    response_id: UUID
    extracted_text: str = (
        "Российская Федерация СТРАХОВОЕ СВИДЕТЕХЬСТВО ОБЯЗАТЕЛЬНОГО ПЕНСИОННОГО "
        "СТРАХОВАНИЯ 038-451-033 48 Ф.и.0 ИВАНОВА СВЕТДАНА ИВАНОВНА Дата и место "
        "рождения 21 августа 1963 года АНГАРСК ИРКУТСКАЯ ОБЛАСТЬ Пол ЖенсКий "
        "Дата регистрации 29 сентября 1998 года"
    )
    llm_corrected_text: str = (
        '{"snils_number": "038-451-033 48", '
        '"last_name": "Иванова", '
        '"name": "Светлана", '
        '"surname": "Ивановна", '
        '"birth_date": "21 августа 1963 года", '
        '"birth_place": "АНГАРСК ИРКУТСКАЯ ОБЛАСТЬ", '
        '"gender": "женский", '
        '"registration_date": "29 сентября 1998 года", '
        '"is_corrected": true, '
        '"corrections": ['
        '  {"original_word": "СВЕТДАНА", "corrected_word": "Светлана"}, '
        '  {"original_word": "ЖенсКий", "corrected_word": "женский"}, '
        '  {"original_word": "ИКУТСКАЯ", "corrected_word": "ИРКУТСКАЯ"}'
        '] }'
    )