import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///trades.db')

# Application Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Server Mappings
SERVER_MAPPINGS = {
    'Har': 'Harmony',
    'Mel': 'Melody',
    'Cad': 'Cadence'
}

# Currency Conversion Rates
CURRENCY_RATES = {
    'gold': 100,    # 1 gold = 100 silver
    'silver': 1,    # 1 silver = 1 silver
    'copper': 0.01, # 1 copper = 0.01 silver
    'iron': 0.0001  # 1 iron = 0.0001 silver
} 