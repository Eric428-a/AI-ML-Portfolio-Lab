from app.core.config import settings
from app.rag.prompt import build_rag_prompt


class LLMService:
    def generate(
        self,
        question: str,
        contexts: list[str],
    ) -> str:
        prompt = build_rag_prompt(
            question=question,
            contexts=contexts,
        )

        if not settings.openai_api_key:
            return (
                "LLM configuration is not available yet. "
                "The retrieved document context was successfully "
                "prepared for this question.\n\n"
                f"{prompt}"
            )

        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=settings.openai_api_key,
            )

            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a document question-answering "
                            "assistant. Answer only from the supplied "
                            "document context."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.1,
            )

            return response.choices[0].message.content or ""

        except Exception as exc:
            return f"LLM request failed: {exc}"


llm_service = LLMService()