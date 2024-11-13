import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        # Drip API Configuration
        self.DRIP_API_BASE_URL = os.getenv("DRIP_API_BASE_URL")
        self.DRIP_API_KEY = os.getenv("HACKATHON_API_KEY")      # <--- Ensure .env is configured properly
        self.DRIP_ACCOUNT_ID = os.getenv("HACKATHON_REALM_ID")  # <--- Ensure .env is configured properly
        
        # OAuth Configuration (for public integrations)
        self.DRIP_CLIENT_ID = "YOUR_CLIENT_ID"
        self.DRIP_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
        self.DRIP_OAUTH_REDIRECT_URI = "YOUR_CALLBACK_URL"
        
        # Database Configuration
        self.DATABASE_PATH = os.getenv("PLAYER_DB_PATH")        # <--- Ensure .env is configured properly

# Create a singleton instance
config = Config()