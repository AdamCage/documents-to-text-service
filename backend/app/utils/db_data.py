from typing import Any, Optional


class DBData:
    """_summary_
    """

    def __init__(
            self,
            request_body: dict[str, Any],
            image_number: int = 0,
            original_image_s3_url: Optional[str] = None,
            processed_image_s3_url: Optional[str] = None,
            extracted_text_s3_url: Optional[str] = None,
            extracted_text: Optional[str] = None,
            llm_prompt: Optional[str] = None,
            llm_response: Optional[str] = None
        ) -> None:
        """_summary_

        Args:
            request_body (dict[str, Any]): _description_
            image_number (int, optional): _description_. Defaults to 0.
            original_image_s3_url (Optional[str], optional): _description_. Defaults to None.
            processed_image_s3_url (Optional[str], optional): _description_. Defaults to None.
            extracted_text_s3_url (Optional[str], optional): _description_. Defaults to None.
            extracted_text (Optional[str], optional): _description_. Defaults to None.
            llm_prompt (Optional[str], optional): _description_. Defaults to None.
            llm_response (Optional[str], optional): _description_. Defaults to None.
        """
        self.request_body = request_body
        self.image_number = image_number
        self.original_image_s3_url = original_image_s3_url
        self.processed_image_s3_url = processed_image_s3_url
        self.extracted_text_s3_url = extracted_text_s3_url
        self.extracted_text = extracted_text
        self.llm_prompt = llm_prompt
        self.llm_response = llm_response
