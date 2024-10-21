import logging
from app.settings import com_settings


com_settings.LOGGING_LEVEL = com_settings.LOGGING_LEVEL.upper()

level = logging.WARNING
if hasattr(logging, com_settings.LOGGING_LEVEL):
    level = getattr(logging, com_settings.LOGGING_LEVEL)

logging.basicConfig(
    level=level,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger(__name__)
log.setLevel(level)

log.debug(f"Got logging level {com_settings.LOGGING_LEVEL} at module {__name__}")

