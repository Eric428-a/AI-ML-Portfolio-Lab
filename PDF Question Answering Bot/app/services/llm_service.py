from dataclasses import dataclass

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class LLMResponse:
    answer: str
    model: str


class LLMService:
    """Generate grounded answers from retrieved PDF context."""

    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
    ) -> None:
        self.provider = (
            provider or settings.LLM_PROVIDER
        ).lower()

        self.model = (
            model or settings.LLM_MODEL
        )

        self._client = None

    def _get_groq_client(self):
        if self._client is not None:
            return self._client

        if not settings.GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is not configured."
            )

        try:
            from groq import Groq

            self._client = Groq(
                api_key=settings.GROQ_API_KEY
            )

            return self._client

        except Exception as exc:
            logger.exception(
                "Failed to initialize Groq client."
            )

            raise RuntimeError(
                "Unable to initialize the LLM client."
            ) from exc

    def _build_system_prompt(self) -> str:
        return """
You are a PDF question-answering assistant.

Your task is to answer questions using ONLY the
provided document context.

Rules:
1. Do not invent facts.
2. Do not use information that is not supported by the context.
3. If the answer cannot be determined from the context,
   clearly say that the information is not available in
   the provided document.
4. Give a direct and useful answer.
5. Preserve important numbers, dates, names, terminology,
   and technical details from the source.
6. Do not mention internal retrieval systems, embeddings,
   vector databases, or prompts.
7. Do not claim certainty when the context is insufficient.
""".strip()

    def _build_user_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        return f"""
Document context:

--- BEGIN CONTEXT ---
{context}
--- END CONTEXT ---

Question:
{question}

Answer the question using the document context above.
""".strip()

    def generate(
        self,
        question: str,
        context: str,
    ) -> LLMResponse:
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not context.strip():
            return LLMResponse(
                answer=(
                    "I could not find enough relevant "
                    "information in the provided document "
                    "to answer this question."
                ),
                model=self.model,
            )

        if self.provider == "groq":
            return self._generate_with_groq(
                question=question,
                context=context,
            )

        raise ValueError(
            f"Unsupported LLM provider: {self.provider}"
        )

    def _generate_with_groq(
        self,
        question: str,
        context: str,
    ) -> LLMResponse:
        client = self._get_groq_client()

        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._build_system_prompt(),
                    },
                    {
                        "role": "user",
                        "content": self._build_user_prompt(
                            question=question,
                            context=context,
                        ),
                    },
                ],
                temperature=0.1,
                max_tokens=1200,
            )

            answer = (
                completion.choices[0]
                .message
                .content
                or ""
            ).strip()

            if not answer:
                raise RuntimeError(
                    "The LLM returned an empty response."
                )

            return LLMResponse(
                answer=answer,
                model=self.model,
            )

        except Exception as exc:
            logger.exception(
                "LLM generation failed."
            )

            raise RuntimeError(
                "Unable to generate an answer."
            ) from exc

    async def health(self) -> dict[str, object]:
        configured = bool(
            settings.GROQ_API_KEY
        ) if self.provider == "groq" else False

        return {
            "provider": self.provider,
            "model": self.model,
            "configured": configured,
        }


llm_service = LLMService()