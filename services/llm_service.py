"""
services/llm_service.py  –  Aeterna CareerForge LLM Service
============================================================
DESIGN:
  _get_client() is called fresh on every public method.
  It checks (in order):
    1. self.client  — explicitly set by the page after init (e.g. llm.client = genai.Client(...))
    2. st.session_state["gemini_api_key"]  — typed into UI
    3. settings.gemini_api_key  — from .env

  This means the page can do:
      llm = LLMService()
      llm.client = genai.Client(api_key=st.session_state["gemini_api_key"])
  and the client is GUARANTEED to be used for every subsequent call.
"""

import time
from typing import Any

from google import genai
from google.genai import types
from loguru import logger

from config.settings import get_settings

DEFAULT_MODEL = "gemini-2.5-flash"


class LLMService:

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client: genai.Client | None = None   # pages can set this directly

    # ── private ──────────────────────────────────────────────────────────────

    def _get_api_key(self) -> str | None:
        try:
            import streamlit as st
            key = st.session_state.get("gemini_api_key", "").strip()
            if key:
                return key
        except Exception:
            pass
        key = (self.settings.gemini_api_key or "").strip()
        return key or None

    def _get_client(self) -> genai.Client | None:
        """
        Returns the client to use, in priority order:
        1. self.client (explicitly injected by the calling page)
        2. A fresh client built from the current session/env key
        """
        if self.client is not None:
            return self.client

        api_key = self._get_api_key()
        if not api_key:
            logger.warning("LLMService: No API key available — mock mode.")
            return None
        try:
            c = genai.Client(api_key=api_key)
            logger.debug("LLMService: built fresh genai.Client from key.")
            return c
        except Exception as e:
            logger.error(f"LLMService: failed to build client: {e}")
            return None

    def _retry(self, fn, max_retries: int = 4):
        for attempt in range(1, max_retries + 1):
            try:
                return fn()
            except Exception as e:
                msg = str(e)
                if ("429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower()) \
                        and attempt < max_retries:
                    wait = min(2 ** attempt + attempt, 30)
                    logger.warning(f"Rate limit – retrying in {wait}s (attempt {attempt}/{max_retries})")
                    time.sleep(wait)
                else:
                    raise

    # ── public ───────────────────────────────────────────────────────────────

    def generate_text(
        self,
        prompt: str,
        system_instruction: str | None = None,
        enable_search: bool = False,
    ) -> str:
        client = self._get_client()
        if client is None:
            return "[MOCK RESPONSE] No Gemini API key configured."

        tools  = [types.Tool(google_search=types.GoogleSearch())] if enable_search else None
        config = types.GenerateContentConfig(tools=tools)
        if system_instruction:
            config.system_instruction = system_instruction

        logger.info(f"generate_text: {len(prompt)} chars, search={enable_search}")
        try:
            def _call():
                r = client.models.generate_content(
                    model=DEFAULT_MODEL, contents=prompt, config=config
                )
                return r.text if r and r.text else "No content generated."
            result = self._retry(_call)
            logger.info("generate_text: OK")
            return result
        except Exception as e:
            logger.error(f"generate_text error: {e}")
            return f"Error: {e}"

    def generate_text_with_history(
        self,
        history: list[dict],
        system_instruction: str | None = None,
    ) -> str:
        """
        Multi-turn conversation.
        history: list of {"role": "user"/"model", "content": "..."} dicts.
        """
        client = self._get_client()
        if client is None:
            return "[MOCK RESPONSE] No Gemini API key configured."

        config = types.GenerateContentConfig()
        if system_instruction:
            config.system_instruction = system_instruction

        contents = [
            types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])],
            )
            for msg in history
        ]

        logger.info(f"generate_text_with_history: {len(contents)} turns")
        try:
            def _call():
                r = client.models.generate_content(
                    model=DEFAULT_MODEL, contents=contents, config=config
                )
                return r.text if r and r.text else "No response generated."
            result = self._retry(_call)
            logger.info("generate_text_with_history: OK")
            return result
        except Exception as e:
            logger.error(f"generate_text_with_history error: {e}")
            return f"Error: {e}"

    def generate_structured_data(
        self,
        prompt: str,
        schema: type,
        system_instruction: str | None = None,
        enable_search: bool = False,
    ) -> Any:
        client = self._get_client()
        if client is None:
            logger.warning("generate_structured_data: no client.")
            return None

        tools  = [types.Tool(google_search=types.GoogleSearch())] if enable_search else None
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            tools=tools,
        )
        if system_instruction:
            config.system_instruction = system_instruction

        logger.info(f"generate_structured_data: schema={schema.__name__}")
        try:
            def _call():
                r = client.models.generate_content(
                    model=DEFAULT_MODEL, contents=prompt, config=config
                )
                if r and r.parsed:
                    return r.parsed
                logger.warning("generate_structured_data: no parsed field.")
                return None
            result = self._retry(_call)
            if result:
                logger.info(f"generate_structured_data: OK ({schema.__name__})")
            return result
        except Exception as e:
            logger.error(f"generate_structured_data error: {e}")
            return None