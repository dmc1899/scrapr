"""
Configuration management.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv


def load_config() -> Dict[str, Any]:
    load_dotenv()
    config = {'SCRAPER_API_URL': os.getenv('SCRAPER_API_URL'), 'SCRAPER_API_KEY': os.getenv('SCRAPER_API_KEY')}

    missing = [key for key, value in config.items() if value is None]
    if missing:
        raise ValueError(f"Missing configuration item: {', '.join(missing)}")

    return config
