import logging
import coloredlogs
from config import Config

def setup_console_logger(name, console_handler, level):
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.addHandler(console_handler)
    logger.setLevel(level)

def setup_logging(config: Config):
    # Create root logger
    root_logger = logging.getLogger()

    # Set up file logging
    if config.log_to_file:
        file_handler = logging.FileHandler(config.log_file_name)
        file_handler.setLevel(getattr(logging, config.file_log_level))
        root_logger.addHandler(file_handler)

    # Set up console logging
    if config.log_to_console:
        console_handler = logging.StreamHandler()
        root_logger.addHandler(console_handler)
        coloredlogs.install(level=config.console_log_level, logger=root_logger)

        # Console-only loggers for langchain and urllib3 - set level to ERROR to avoid console spam
        setup_console_logger('langchain', console_handler, logging.CRITICAL)
        setup_console_logger('urllib3', console_handler, logging.CRITICAL)
        
    # Set up document retrieval logger
    if config.log_doc_retrieval:
        doc_retrieval_logger = logging.getLogger('doc_retrieval')
        doc_retrieval_handler = logging.FileHandler(config.doc_retrieval_log_file_name)
        doc_retrieval_handler.setLevel(getattr(logging, config.doc_retrieval_log_level))
        doc_retrieval_logger.addHandler(doc_retrieval_handler)

    return root_logger
