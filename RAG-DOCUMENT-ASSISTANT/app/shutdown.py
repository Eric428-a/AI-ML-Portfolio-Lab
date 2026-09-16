import logging

logger = logging.getLogger(__name__)


async def shutdown() -> None:
    logger.info("Shutting down RAG Document Assistant")