"""Class and methods for app config."""
import os
import yaml
from dotenv import load_dotenv

dotenv_path = "../.env"


class Config:
    _instance = None # Holds single instance of Config once created

    def __new__(cls, filename):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load(filename)
            load_dotenv(dotenv_path)  # Load environment variables from .env file
        return cls._instance

    def _load(self, filename):
        with open(filename, 'r') as file:
            self.config = yaml.safe_load(file)
        self._load_from_env()

    def _load_from_env(self):
        for key in self.config:
            env_value = os.getenv(key.upper())
            if env_value is not None:
                self.config[key] = type(self.config[key])(env_value)

    @property
    def filepath(self):
        return self.config.get("document_path")

    @property
    def split_method(self):
        return self.config.get("split_method")

    @property
    def chunk_size(self):
        return self.config.get("chunk_size")

    @property
    def chunk_overlap(self):
        return self.config.get("chunk_overlap")

    def get_config_value(self, key):
        # Get configuration value from key name (e.g. filename)
        return self.config.get(key)

    def get_env_value(self, key):
        # Get environment variable from key name (e.g. OPENAI_API_KEY)
        return os.getenv(key)
    