import os
import logging
from fastapi import HTTPException, status
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded, GoogleAPIError
import google.generativeai as genai

logger = logging.getLogger(__name__)

PLACEHOLDER_KEYS = {
    "your-gemini-api-key-here",
    "paste_your_key_locally",
}

def is_unconfigured_key(key: str | None) -> bool:
    if not key or not key.strip():
        return True
    cleaned = key.strip().lower()
    return cleaned in PLACEHOLDER_KEYS or "your-key" in cleaned or "paste_your" in cleaned

def generate_task_description(title: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if is_unconfigured_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini API key is not configured"
        )
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Write a concise, professional task description for the following task title. Do not include extra pleasantries.\n\nTitle: {title}"
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip() if getattr(response, "text", None) else ""
        if not text:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Gemini API returned an empty response"
            )
        return text
    except HTTPException:
        raise
    except ResourceExhausted:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Gemini API rate limit exceeded")
    except DeadlineExceeded:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Gemini API timeout")
    except GoogleAPIError as e:
        logger.error(f"Gemini API Error: {e}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to communicate with Gemini API")
    except Exception as e:
        logger.error(f"Unexpected error calling Gemini: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while generating the description")
