"""Simple file logger used by the localization example scripts."""

import logging
import os
from datetime import datetime

def setup_logger(name='localization', log_dir='logs', level=logging.INFO):
    """Initializes a logger that logs to both file and console."""
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(log_dir, f'{name}_{timestamp}.log')

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if re-imported
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)

        # Add both handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.info(f"Logger initialized. Writing to {log_file}")

    return logger