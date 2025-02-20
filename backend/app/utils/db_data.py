from typing import Any, Optional


class DBData:
    """_summary_
    """

    def __init__(
            self,
            request_body: dict[str, Any],
            original_image_s3_url: Optional[str] = None,
            processed_image_s3_url: Optional[str] = None,
            extracted_text_s3_url: Optional[str] = None,
            extracted_text: Optional[str] = None
        ) -> None:
        """_summary_

        Args:
            request_body (dict[str, Any]): _description_
            original_image_s3_url (str): _description_
            processed_image_s3_url (str): _description_
            extracted_text (str): _description_
            response_body (dict[str, Any]): _description_
        """
        self.request_body = request_body
        self.original_image_s3_url = original_image_s3_url
        self.processed_image_s3_url = processed_image_s3_url
        self.extracted_text_s3_url = extracted_text_s3_url
        self.extracted_text = extracted_text
