import sys
from pathlib import Path
from loguru import logger

def configure_logger(log_level: str = "INFO", log_file: str = "logs/app.log") -> None:
    """
    Configures Loguru logger.
    Sets up console logging and persistent file logging with rotation.
    """
    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        enqueue=True
    )

    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Add file handler
    logger.add(
        str(log_path),
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True
    )

    logger.info(f"Centralized logger initialized at level: {log_level}, writing to: {log_file}")
