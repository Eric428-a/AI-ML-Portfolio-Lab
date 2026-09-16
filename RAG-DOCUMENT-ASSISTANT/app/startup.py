import logging

from app.core.config import settings
from app.core.logging import configure_logging

logger = logging.getLogger(__name__)


async def startup() -> None:
    configure_logging()

    logger.info(
        "Starting %s v%s",
        settings.app_name,
        settings.app_version,
    )