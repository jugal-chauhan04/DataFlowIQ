import logging
import os

def setup_logging(log_file = 'pipeline.log'):
    """
    Configure logging to include timestamps, duration, and messages
    """

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

    logging.info("Logging Initialized")