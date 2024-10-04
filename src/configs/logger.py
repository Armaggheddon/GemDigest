import os
import logging
from datetime import datetime

def setup_logger() -> logging.Logger:
    """
    Set up and configure a logger for logging messages.

    The function creates a logger that outputs messages to a file in the 'log' 
    directory. The log file is named based on the current year and month.

    Returns:
        logging.Logger: The configured logger.

    Example:
        Add the following code to the top of a file to configure a 
            logger for that file.
        setup_logger()
        logger = logging.getLogger(__name__)

        Add one of the following code to log a message.
        logger.info("This is an info message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.debug("This is a debug message.")
        logging.critical("This is a critical message.")
    """
    pre_format = '%(asctime)s :: [%(levelname)-8s]'
    post_format = '[%(filename)s] - [%(funcName)s : %(lineno)s] - %(message)s'

    format = pre_format + ' - ' + post_format
    # Configure logging to output messages to a file
    logging.basicConfig(level=logging.INFO,
                        format=format,
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    # logging.getLogger('asyncio').setLevel(logging.ERROR)
    # logging.getLogger('aiohttp').setLevel(logging.ERROR)

    logger = logging.getLogger()
    return logger