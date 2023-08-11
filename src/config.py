"""Module for handling the application's configuration.

This module provides the Config class, which manages the loading and access of the application's settings from a YAML file and environment variables.
"""
import os
import yaml
import logging
from dotenv import load_dotenv


class Config:
    """Singleton class for managing the application's configuration.

    This class is responsible for loading the configuration from a YAML file
    and providing access to specific configuration values. It also manages
    environment variables from a .env file.

    Attributes:
        _instance: Singleton instance of the Config class.
    """

    _instance = None

    def __new__(cls, filename):
        """Ensure a single instance of Config and load the configuration."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            try:
                cls._instance._load(filename)
            except Exception as e:
                logging.error(f"Failed to load configuration: {e}")
        return cls._instance

    def _load(self, filename):
        """Load the configuration from a YAML file and environment variables."""
        with open(filename, "r") as file:
            self.config = yaml.safe_load(file)
        
        # Get the env_path, or None if it's not set
        env_path = self.config.get("env_path", None)
        if env_path:
            load_dotenv(env_path)

    # Below are properties that provide access to specific configuration values.
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
    def llm_model(self):
        return self.config.get("llm_model")

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
        """Get configuration value from key name (e.g. filename)."""
        return self.config.get(key)

    def get_env_value(self, key):
        """Get environment variable from key name (e.g. OPENAI_API_KEY)"""
        return os.getenv(key)

    # Below are setters that provide access to changing specific configuration values.
    @llm_model.setter
    def llm_model(self, value):
        self._llm_model = value

    @chunk_size.setter
    def chunk_size(self, value):
        self._chunk_size = value

    @chunk_overlap.setter
    def chunk_overlap(self, value):
        self._chunk_overlap = value

    @temperature.setter
    def temperature(self, value):
        self._temperature = value
