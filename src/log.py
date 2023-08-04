import logging
import coloredlogs
from config import Config

def setup_console_logger(name, console_handler, level):
    """
    Sets up a console-only logger.

    Args:
        name (str): The name of the logger.
        console_handler (logging.Handler): The handler for console output.
        level (str): The logging level for the logger.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.addHandler(console_handler)
    logger.setLevel(getattr(logging, level))

def setup_logging(config: Config):
    """
    Sets up the logging configuration.

    Args:
        config (Config): The application configuration.

    Returns:
        logging.Logger: The root logger.
    """
    # Create root logger
    root_logger = logging.getLogger()

    # Set up file logging
    if config.log_to_file:
        try:
            file_handler = logging.FileHandler(config.log_file_name)
            file_handler.setLevel(getattr(logging, config.file_log_level))
            root_logger.addHandler(file_handler)
        except Exception as e:
            root_logger.warning(f"Could not set up file logging: {e}")

    # Set up console logging
    if config.log_to_console:
        console_handler = logging.StreamHandler()
        root_logger.addHandler(console_handler)
        coloredlogs.install(level=config.console_log_level, logger=root_logger)

        # Console-only loggers for langchain and urllib3 - default level to ERROR/CRITICAL to avoid console spam
        setup_console_logger('langchain', console_handler, 'CRITICAL')
        setup_console_logger('urllib3', console_handler, 'ERROR')
        setup_console_logger('faiss', console_handler, 'ERROR')
        
    # Set up document retrieval logger
    if config.log_doc_retrieval:
        try:
            doc_retrieval_logger = logging.getLogger('doc_retrieval')
            doc_retrieval_handler = logging.FileHandler(config.doc_retrieval_log_file_name)
            doc_retrieval_handler.setLevel(getattr(logging, config.doc_retrieval_log_level))
            doc_retrieval_logger.addHandler(doc_retrieval_handler)
            doc_retrieval_logger.propagate = False
        except Exception as e:
            root_logger.warning(f"Could not set up document retrieval logging: {e}")

    return root_logger
