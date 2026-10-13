import logging
from functools import lru_cache

from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        if self.provider == "none":
            return (
                "No language model is configured. "
                "Configure LLM_PROVIDER and its API credentials "
                "to generate grounded answers."
            )

        if self.provider == "groq":
            return self._generate_openai_compatible(
                base_url=settings.LLM_BASE_URL or "https://api.groq.com/openai/v1",
                api_key=settings.LLM_API_KEY,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

        if self.provider == "openai":
            return self._generate_openai_compatible(
                base_url=settings.LLM_BASE_URL or "https://api.openai.com/v1",
                api_key=settings.LLM_API_KEY,
                model=self.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

        if self.provider == "ollama":
            return self._generate_ollama(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

        raise RuntimeError(
            f"Unsupported language model provider: {self.provider}"
        )

    def _generate_openai_compatible(
        self,
        base_url: str,
        api_key: str,
        model: str,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        if not api_key:
            raise RuntimeError(
                f"LLM_API_KEY is required for provider '{self.provider}'."
            )

        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=api_key,
                base_url=base_url,
                timeout=settings.LLM_TIMEOUT_SECONDS,
                max_retries=2,
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
            )

            answer = response.choices[0].message.content

            if not answer:
                raise RuntimeError("The language model returned an empty answer.")

            return answer.strip()

        except Exception as exc:
            logger.exception("LLM generation failed")
            raise RuntimeError(f"Language model request failed: {exc}") from exc

    def _generate_ollama(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        try:
            import httpx

            base_url = (
                settings.LLM_BASE_URL.rstrip("/")
                if settings.LLM_BASE_URL
                else "http://localhost:11434"
            )

            response = httpx.post(
                f"{base_url}/api/chat",
                json={
                    "model": self.model,
                    "stream": False,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    "options": {
                        "temperature": settings.LLM_TEMPERATURE,
                    },
                },
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )

            response.raise_for_status()
            data = response.json()

            answer = data.get("message", {}).get("content", "")

            if not answer:
                raise RuntimeError("Ollama returned an empty answer.")

            return answer.strip()

        except Exception as exc:
            logger.exception("Ollama generation failed")
            raise RuntimeError(f"Ollama request failed: {exc}") from exc


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService()