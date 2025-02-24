import re
import logging
from typing import Optional

import httpx
from dotenv import dotenv_values

from core import config, DocumentCodeLLMPromtMap
from validation_models import LLMRequest, LLMResponse


async def llm_correction_pipeline(
        raw_text: str,
        document_type_code: int,
        logger: logging.Logger,
        custom_prompt: Optional[str] = None
    ) -> str:
    
    llm_service_config = dotenv_values()
    llm_url = f"{llm_service_config.get("LLM_HOST")}:{llm_service_config.get("LLM_PORT")}{llm_service_config.get("LLM_ENDPOINT")}"

    prompt = custom_prompt if custom_prompt else DocumentCodeLLMPromtMap.get_prompt(document_type_code)
    prompt += f'```\n{raw_text}\n```'

    verify_ssl = config.llm_config.get("cert_path")

    payload = LLMRequest(
        stream=config.llm_config["llm_request_params"]["stream"],
        model=config.llm_config["llm_request_params"]["model"],
        format=config.llm_config["llm_request_params"]["format"],
        prompt=prompt
    )

    msg = f'Sending request to LLM-service to correct document with code {document_type_code}'
    if custom_prompt:
        msg += f'. Custom prompt: ```\n{custom_prompt}\n```'
    logger.info(msg)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                llm_url,
                json=payload.model_dump(),
                timeout=60 * 3
            )
        
        response.raise_for_status()
        response_data = response.json()
        
        llm_response = LLMResponse(**response_data)
        
        processed_text = re.sub(r'<think>.*?</think>', '', llm_response.response, flags=re.DOTALL)
        
        return processed_text

    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    except Exception as e:
        error_msg = f"LLM processing failed: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
