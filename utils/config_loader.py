"""config_loader.py - Configuration management for the HVAC Assistant pipeline"""

import yaml
from pathlib import Path
from typing import Dict, Any
from functools import lru_cache


@lru_cache(maxsize=1)
def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml file.
    
    Uses LRU cache to ensure config is only loaded once per process.
    
    Returns:
        Dict containing configuration settings
    """
    config_path = Path(__file__).parent.parent / "config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_spark_config() -> Dict[str, Any]:
    """Get Spark configuration settings."""
    config = load_config()
    return config.get('spark', {})


def get_scraping_config() -> Dict[str, Any]:
    """Get web scraping configuration settings."""
    config = load_config()
    return config.get('scraping', {})


def get_pdf_processing_config() -> Dict[str, Any]:
    """Get PDF processing configuration settings."""
    config = load_config()
    return config.get('pdf_processing', {})


def get_embeddings_config() -> Dict[str, Any]:
    """Get embeddings configuration settings."""
    config = load_config()
    return config.get('embeddings', {})


def get_retrieval_config() -> Dict[str, Any]:
    """Get retrieval configuration settings."""
    config = load_config()
    return config.get('retrieval', {})


def get_paths() -> Dict[str, str]:
    """Get path configuration settings."""
    config = load_config()
    return config.get('paths', {})


def get_path(key: str) -> str:
    """Get a specific path from configuration.
    
    Args:
        key: Path key from config.yaml
        
    Returns:
        Path string
        
    Raises:
        KeyError: If path key not found in configuration
    """
    paths = get_paths()
    if key not in paths:
        raise KeyError(f"Path '{key}' not found in configuration")
    return paths[key]


def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration settings."""
    config = load_config()
    return config.get('logging', {})