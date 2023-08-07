"""Class and methods for app config"""
import os
import yaml
import logging
from dotenv import load_dotenv


class Config:
    _instance = None  # Holds single instance of Config once created

    def __new__(cls, filename):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            try:
                cls._instance._load(filename)
            except Exception as e:
                logging.error(f"Failed to load configuration: {e}")
        return cls._instance

    def _load(self, filename):
        with open(filename, "r") as file:
            self.config = yaml.safe_load(file)
        load_dotenv(
            self.config.get("env_path")
        )  # Load environment variables from .env file

    @property
    def debug(self):
        return self.config.get("debug")

    @property
    def document_paths(self):
        return self.config.get("document_paths")

    @property
    def split_method(self):
        return self.config.get("split_method")

    @property
    def chunk_size(self):
        return self.config.get("chunk_size")

    @property
    def chunk_overlap(self):
        return self.config.get("chunk_overlap")

    @property
    def temperature(self):
        return self.config.get("temperature")

    @property
    def log_to_console(self):
        return self.config.get("log_to_console")

    @property
    def console_log_color(self):
        return self.config.get("console_log_color")

    @property
    def log_to_file(self):
        return self.config.get("log_to_file")

    @property
    def log_file_name(self):
        return self.config.get("log_file_name")

    @property
    def console_log_level(self):
        return self.config.get("console_log_level")

    @property
    def file_log_level(self):
        return self.config.get("file_log_level")

    # Logging - document retrieval
    @property
    def log_doc_retrieval(self):
        return self.config.get("log_doc_retrieval")

    @property
    def doc_retrieval_log_file_name(self):
        return self.config.get("doc_retrieval_log_file_name")

    @property
    def doc_retrieval_log_level(self):
        return self.config.get("doc_retrieval_log_level")

    def get_config_value(self, key):
        # Get configuration value from key name (e.g. filename)
        return self.config.get(key)

    def get_env_value(self, key):
        # Get environment variable from key name (e.g. OPENAI_API_KEY)
        return os.getenv(key)
